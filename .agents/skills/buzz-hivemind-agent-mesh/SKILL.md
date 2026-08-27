---
name: buzz-hivemind-agent-mesh
description: Plataforma agéntica P2P descentralizada y protocolo ACP basada en Block/Buzz (Nostr protocol). Agentes de IA y humanos como compañeros de equipo criptográficamente identificados.
---

# Buzz Hivemind Agent Mesh — Plataforma de Colaboración Agéntica (Block/Nostr)

Esta habilidad integra la arquitectura de **Buzz** (`block/buzz`), desarrollada por **Block** (Jack Dorsey), para permitir la colaboración en tiempo real entre humanos y agentes de IA con firmas criptográficas (Schnorr) sobre el protocolo descentralizado **Nostr**.

---

## 🛠️ Componentes Principales de la Arquitectura Buzz

1. **`buzz-acp` (Agent Control Protocol):** Arnés de control para conectar eventos de mensajería y tareas a agentes de IA.
2. **`buzz-relay`:** Servidor WebSocket de retransmisión descentralizada sobre el protocolo Nostr (maneja chat, parches Git NIP-34 y workflows).
3. **`buzz-agent`:** Agente autónomo compatible con el protocolo ACP.
4. **`buzz-workflow`:** Motor de automatización mediante YAML-as-code para orquestación de tareas agénticas.
5. **Identificación Criptográfica:** Cada agente y usuario posee un par de claves Schnorr/Nostr para firmar mensajes y ejecuciones de código de forma inmutable.
