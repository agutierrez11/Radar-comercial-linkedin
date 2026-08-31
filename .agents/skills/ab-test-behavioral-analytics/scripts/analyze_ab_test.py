import argparse
import math
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description="Analizador de Significancia Estadística A/B")
    parser.add_argument("--sent_a", type=int, required=True, help="Enviados Variante A")
    parser.add_argument("--conv_a", type=int, required=True, help="Conversiones/Respuestas Variante A")
    parser.add_argument("--sent_b", type=int, required=True, help="Enviados Variante B")
    parser.add_argument("--conv_b", type=int, required=True, help="Conversiones/Respuestas Variante B")

    args = parser.parse_args()

    rate_a = args.conv_a / args.sent_a
    rate_b = args.conv_b / args.sent_b

    # Pooled probability
    p_pool = (args.conv_a + args.conv_b) / (args.sent_a + args.sent_b)
    se_pool = math.sqrt(p_pool * (1 - p_pool) * (1/args.sent_a + 1/args.sent_b))

    z_score = (rate_b - rate_a) / se_pool if se_pool > 0 else 0
    # Two-tailed p-value approximation
    p_value = 2 * (1 - 0.5 * (1 + math.erf(abs(z_score) / math.sqrt(2))))

    uplift = ((rate_b - rate_a) / rate_a) * 100 if rate_a > 0 else 0

    print("=" * 60)
    print("📊 RESULTADOS DEL ANÁLISIS CONDUCTUAL DE PRUEBA A/B")
    print("=" * 60)
    print(f"Variante A: {args.conv_a}/{args.sent_a} ({rate_a*100:.2f}%)")
    print(f"Variante B: {args.conv_b}/{args.sent_b} ({rate_b*100:.2f}%)")
    print(f"Mejora relativa (Uplift): {uplift:+.2f}%")
    print(f"Z-Score: {z_score:.4f}")
    print(f"P-Value: {p_value:.4f}")
    print("-" * 60)

    if p_value < 0.05:
        winner = "Variante B" if rate_b > rate_a else "Variante A"
        print(f"🎉 ¡RESULTADO ESTADÍSTICAMENTE SIGNIFICATIVO (p < 0.05)!")
        print(f"🏆 Ganador indiscutible: {winner}. Se recomienda escalar masivamente esta variante.")
    else:
        print("⚠️ No hay significancia estadística suficiente aún (p >= 0.05).")
        print("   Recomendación: Continuar la prueba hasta acumular más muestras.")
    print("=" * 60)

if __name__ == "__main__":
    main()
