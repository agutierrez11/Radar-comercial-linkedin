/*
 * Radar Comercial — núcleo local-first de búsqueda.
 *
 * Esta primera versión no envía datos a ningún servicio externo. Recibe la
 * bóveda activa en memoria y devuelve resultados explicables. El dashboard
 * puede seguir usando el dataset curado y, cuando exista, messages.csv.
 */
(function (global) {
  'use strict';

  const STOPWORDS = new Set([
    'a', 'al', 'con', 'como', 'de', 'del', 'en', 'entre', 'el', 'ella',
    'ellos', 'esta', 'este', 'hay', 'la', 'las', 'lo', 'los', 'me', 'mi',
    'mis', 'para', 'por', 'que', 'se', 'sin', 'su', 'sus', 'tu', 'tus',
    'un', 'una', 'unos', 'unas', 'y', 'yo', 'de', 'mi'
  ]);

  const SYNONYMS = {
    bata: ['bata', 'batas', 'quirurgica', 'quirurgicas', 'surgical gown', 'medical gown'],
    cubrebocas: ['cubrebocas', 'mascarilla', 'mascarillas', 'kn95', 'n95', 'tapabocas', 'barbijo'],
    epp: ['epp', 'ppe', 'equipo de proteccion personal', 'proteccion sanitaria'],
    pagos: ['pago', 'pagos', 'payment', 'payments', 'fintech', 'gateway', 'adquirencia', 'adquirente', 'wallet', 'checkout'],
    venta: ['venta', 'vender', 'vendiendo', 'oferta', 'ofreci', 'pitch', 'propuesta', 'cotizacion', 'precio'],
    respuesta: ['respuesta', 'respondio', 'respondio', 'reply', 'replied', 'interes', 'interesado', 'interesada'],
    reunion: ['reunion', 'llamada', 'demo', 'meeting', 'agenda']
  };

  function normalizeText(value) {
    return String(value == null ? '' : value)
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .replace(/[^a-z0-9@./:+-]+/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function getValue(row, keys) {
    if (!row) return '';
    const list = Array.isArray(keys) ? keys : [keys];
    for (const key of list) {
      if (row[key] != null && String(row[key]).trim() !== '') return String(row[key]);
    }
    const normalizedKeys = Object.keys(row).reduce((acc, key) => {
      acc[normalizeText(key).replace(/ /g, '')] = key;
      return acc;
    }, {});
    for (const key of list) {
      const normalizedKey = normalizeText(key).replace(/ /g, '');
      const originalKey = normalizedKeys[normalizedKey];
      if (originalKey && row[originalKey] != null && String(row[originalKey]).trim() !== '') {
        return String(row[originalKey]);
      }
    }
    return '';
  }

  function parseDate(value) {
    const raw = String(value || '').trim();
    if (!raw) return null;
    const date = new Date(raw.length === 10 ? `${raw}T00:00:00` : raw);
    return Number.isNaN(date.getTime()) ? null : date;
  }

  function ownerMatcher(ownerName) {
    const owner = normalizeText(ownerName);
    const parts = owner.split(' ').filter(part => part.length > 2);
    return function isOwner(sender) {
      const value = normalizeText(sender);
      if (!value || !parts.length) return false;
      const firstMatches = value.includes(parts[0]);
      const lastMatches = parts.slice(1).some(part => value.includes(part));
      return firstMatches && (parts.length === 1 || lastMatches);
    };
  }

  function expandTerm(term) {
    const normalized = normalizeText(term);
    for (const [canonical, values] of Object.entries(SYNONYMS)) {
      if (canonical === normalized || values.includes(normalized)) {
        return [canonical].concat(values);
      }
    }
    return [normalized];
  }

  function parseQuery(input) {
    const raw = String(input || '').trim();
    const normalized = normalizeText(raw);
    const years = (normalized.match(/\b(19|20)\d{2}\b/g) || []).map(Number);
    let direction = null;
    if (/\b(yo ofreci|yo vendi|yo vend|mi pitch|mis mensajes|enviados por mi|lo que vendi)\b/.test(normalized)) {
      direction = 'sent';
    } else if (/\b(me vend|me ofreci|me ofrecieron|inbound|lo que me vendieron)\b/.test(normalized)) {
      direction = 'received';
    }

    const plain = normalized
      .replace(/\b(19|20)\d{2}\b/g, ' ')
      .replace(/\b(yo ofreci|yo vendi|yo vend|mi pitch|mis mensajes|enviados por mi|lo que vendi|me vend|me ofreci|me ofrecieron|inbound|lo que me vendieron)\b/g, ' ')
      .replace(/[^a-z0-9@./:+-]+/g, ' ')
      .trim();

    const baseTerms = plain.split(' ')
      .map(normalizeText)
      .filter(term => term.length > 1 && !STOPWORDS.has(term));
    const terms = [];
    baseTerms.forEach(term => expandTerm(term).forEach(expanded => {
      if (expanded && !terms.includes(expanded)) terms.push(expanded);
    }));

    return { raw, normalized, years, direction, baseTerms, terms };
  }

  function messageText(row) {
    return [
      getValue(row, ['CONTENT', 'CONTENT BODY', 'content', 'text', 'body']),
      getValue(row, ['SUBJECT', 'subject']),
      getValue(row, ['ATTACHMENTS', 'attachments'])
    ].filter(Boolean).join(' ');
  }

  function messageDate(row) {
    return getValue(row, ['DATE', 'date', 'timestamp', 'created_at']);
  }

  function conversationKey(row) {
    return getValue(row, ['CONVERSATION ID', 'Conversation ID', 'conversation_id', 'conversationId']) ||
      `${getValue(row, ['FROM', 'from'])}|${getValue(row, ['TO', 'to'])}`;
  }

  function contactBlob(contact) {
    return normalizeText([
      contact.name, contact.full_name, contact.first_name, contact.last_name,
      contact.company, contact.position, contact.country, contact.city,
      contact.crmNotes, contact.last_msg_snippet, contact.last_reply_snippet,
      contact.message_summary, contact.message_keywords, contact.campaign
    ].filter(Boolean).join(' '));
  }

  function contactNameFromRows(rows, contacts) {
    const contactIndex = new Map();
    (contacts || []).forEach(contact => {
      const name = normalizeText(contact.name || contact.full_name || `${contact.first_name || ''} ${contact.last_name || ''}`);
      const url = normalizeText(contact.url || contact.profile_url || contact.linkedin_url);
      if (name) contactIndex.set(name, contact);
      if (url) contactIndex.set(url, contact);
    });

    for (const row of rows) {
      const candidates = [
        getValue(row, ['TO', 'RECIPIENT NAME', 'to']),
        getValue(row, ['FROM', 'SENDER NAME', 'from'])
      ];
      for (const candidate of candidates) {
        const found = contactIndex.get(normalizeText(candidate));
        if (found) return found;
      }
    }
    return null;
  }

  function dateMatches(query, rowDate) {
    if (!query.years.length) return true;
    const date = parseDate(rowDate);
    return !!date && query.years.includes(date.getFullYear());
  }

  function termsMatched(query, blob) {
    const matches = [];
    query.baseTerms.forEach(term => {
      const expanded = expandTerm(term);
      if (expanded.some(value => blob.includes(value))) matches.push(term);
    });
    return matches;
  }

  function buildConversationIndex(messages, contacts, ownerName) {
    const isOwner = ownerMatcher(ownerName);
    const groups = new Map();

    (messages || []).forEach(row => {
      const key = conversationKey(row);
      if (!key) return;
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(row);
    });

    return Array.from(groups.entries()).map(([id, rows]) => {
      const ordered = rows.slice().sort((a, b) => {
        const da = parseDate(messageDate(a));
        const db = parseDate(messageDate(b));
        return (da ? da.getTime() : 0) - (db ? db.getTime() : 0);
      });
      const texts = ordered.map(messageText).filter(Boolean);
      const fullText = normalizeText(texts.join(' '));
      const sentRows = ordered.filter(row => isOwner(getValue(row, ['FROM', 'SENDER NAME', 'from'])));
      const receivedRows = ordered.filter(row => !isOwner(getValue(row, ['FROM', 'SENDER NAME', 'from'])));
      const dates = ordered.map(row => parseDate(messageDate(row))).filter(Boolean);
      const contact = contactNameFromRows(ordered, contacts);
      const firstMessage = ordered[0] || {};
      const lastMessage = ordered[ordered.length - 1] || {};

      return {
        id,
        rows: ordered,
        text: fullText,
        participant: contact ? (contact.name || contact.full_name) : getValue(firstMessage, ['TO', 'RECIPIENT NAME', 'to']) || 'Conversación',
        contact,
        messageCount: ordered.length,
        sentCount: sentRows.length,
        receivedCount: receivedRows.length,
        firstDate: dates[0] ? dates[0].toISOString() : messageDate(firstMessage),
        lastDate: dates[dates.length - 1] ? dates[dates.length - 1].toISOString() : messageDate(lastMessage),
        firstMessage: messageText(firstMessage),
        lastMessage: messageText(lastMessage),
        commercialDirection: sentRows.length && receivedRows.length ? 'bidireccional' : sentRows.length ? 'enviado' : 'recibido',
        hasAttachments: ordered.some(row => Boolean(getValue(row, ['ATTACHMENTS', 'attachments']).trim()))
      };
    });
  }

  function scoreResult(query, matchedTerms, record, source) {
    const termScore = query.baseTerms.length ? (matchedTerms.length / query.baseTerms.length) * 70 : 0;
    const recencyScore = record.lastDate ? 10 : 0;
    const sourceScore = source === 'conversation' ? 20 : 10;
    const directionScore = query.direction && record.commercialDirection === (query.direction === 'sent' ? 'enviado' : 'recibido') ? 10 : 0;
    return Math.min(100, Math.round(termScore + recencyScore + sourceScore + directionScore));
  }

  function searchVault(options) {
    const opts = options || {};
    const contacts = Array.isArray(opts.contacts) ? opts.contacts : [];
    const messages = Array.isArray(opts.messages) ? opts.messages : [];
    const ownerName = opts.ownerName || '';
    const query = parseQuery(opts.query || '');
    const conversationIndex = buildConversationIndex(messages, contacts, ownerName);
    const results = [];

    conversationIndex.forEach(conversation => {
      if (!dateMatches(query, conversation.firstDate) && !dateMatches(query, conversation.lastDate)) return;
      const matchedTerms = termsMatched(query, conversation.text);
      const directionMatches = !query.direction ||
        (query.direction === 'sent' && conversation.sentCount > 0) ||
        (query.direction === 'received' && conversation.receivedCount > 0);
      if (!matchedTerms.length && query.baseTerms.length) return;
      if (!directionMatches) return;
      results.push({
        type: 'conversation',
        source: 'messages.csv',
        id: conversation.id,
        contact: conversation.contact,
        participant: conversation.participant,
        messageCount: conversation.messageCount,
        firstDate: conversation.firstDate,
        lastDate: conversation.lastDate,
        commercialDirection: conversation.commercialDirection,
        firstMessage: conversation.firstMessage,
        lastMessage: conversation.lastMessage,
        hasAttachments: conversation.hasAttachments,
        matchedTerms,
        score: scoreResult(query, matchedTerms, conversation, 'conversation'),
        reason: `Coincide en ${matchedTerms.join(', ') || 'la fecha'} dentro de ${conversation.messageCount} mensajes.`
      });
    });

    contacts.forEach(contact => {
      const blob = contactBlob(contact);
      const matchedTerms = termsMatched(query, blob);
      const contactDate = contact.last_msg_date || contact.connected_on || contact.updated_at || '';
      if (!dateMatches(query, contactDate)) return;
      if (query.baseTerms.length && !matchedTerms.length) return;
      const contactDirection = contact.is_they_selling ? 'recibido' : contact.msg_count ? 'bidireccional' : null;
      if (query.direction === 'received' && contactDirection !== 'recibido') return;
      results.push({
        type: 'contact',
        source: messages.length ? 'contact-index' : 'curated-data',
        id: contact.id || contact.url || contact.profile_url || `${contact.name}|${contact.company}`,
        contact,
        participant: contact.name || contact.full_name || 'Contacto',
        company: contact.company || '',
        position: contact.position || '',
        lastDate: contactDate,
        matchedTerms,
        score: scoreResult(query, matchedTerms, { lastDate: contactDate, commercialDirection: contactDirection }, 'contact'),
        reason: `Coincide en ${matchedTerms.join(', ') || 'los campos de la ficha'} de la bóveda.`
      });
    });

    const seen = new Set();
    const deduplicated = results.filter(result => {
      const key = `${result.type}:${result.id}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    }).sort((a, b) => b.score - a.score || String(b.lastDate).localeCompare(String(a.lastDate)));

    return {
      query,
      hasFullMessages: messages.length > 0,
      conversationsIndexed: conversationIndex.length,
      results: deduplicated,
      counts: {
        total: deduplicated.length,
        conversations: deduplicated.filter(result => result.type === 'conversation').length,
        contacts: deduplicated.filter(result => result.type === 'contact').length
      }
    };
  }

  function summarizeSearch(result) {
    const data = result || { counts: { total: 0, conversations: 0, contacts: 0 }, hasFullMessages: false };
    return {
      title: `${data.counts.total} resultados`,
      subtitle: data.hasFullMessages ? 'Búsqueda en conversaciones completas y contactos.' : 'Búsqueda en datos curados; carga messages.csv para ver el historial completo.',
      counts: data.counts
    };
  }

  global.RadarCore = {
    version: '0.1.0',
    normalizeText,
    parseQuery,
    buildConversationIndex,
    searchVault,
    summarizeSearch
  };
})(window);
