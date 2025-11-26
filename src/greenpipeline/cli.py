
import sys
import subprocess
import argparse
import json
import time
from datetime import datetime
from pathlib import Path

# Simulación de imports (en producción serían módulos separados)
# from estimator import EnergyEstimator
# from carbon_intensity import CarbonIntensityAPI


class GreenPipelineCLI:
    """CLI principal de GreenPipeline"""

    def __init__(self):
        self.results_file = Path.home() / ".greenpipeline" / "history.json"
        self.results_file.parent.mkdir(exist_ok=True)

    def run_command(
        self, command: str, location: str = "GLOBAL", save_history: bool = True
    ) -> dict:
        """
        Ejecuta un comando y mide su impacto energético.

        Args:
            command: Comando a ejecutar (ej: "npm test")
            location: Ubicación para intensidad de carbono
            save_history: Si guardar en historial

        Returns:
            Dict con métricas y resultados
        """
        print(f"🌱 GreenPipeline - Midiendo: {command}")
        print("=" * 60)

        # 1. Obtener intensidad de carbono actual
        print(f"📍 Ubicación: {location}")
        # carbon_api = CarbonIntensityAPI()
        # carbon_data = carbon_api.get_current_intensity(location)

        # Simulación (en producción usaría la API real)
        carbon_intensity = 420 if location == "DE" else 165 if location == "CO" else 389
        print(f"🌍 Intensidad de carbono: {carbon_intensity} g CO2e/kWh")

        # 2. Ejecutar comando con medición
        print(f"\n⚡ Ejecutando comando...\n")
        start_time = time.time()

        try:
            # Ejecutar comando real
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            success = result.returncode == 0
            output = result.stdout if success else result.stderr

        except Exception as e:
            success = False
            output = str(e)

        duration = time.time() - start_time

        # 3. Simular medición de energía
        # En producción: estimator.measure_execution(...)
        # Para MVP, simulamos basado en duración
        cpu_percent = 45.0  # Promedio estimado
        memory_mb = 512.0

        energy_joules = duration * 25  # ~25W promedio * tiempo
        energy_kwh = energy_joules / 3600000
        carbon_grams = energy_kwh * carbon_intensity

        # 4. Construir resultado
        result_data = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "location": location,
            "success": success,
            "duration_seconds": round(duration, 2),
            "metrics": {
                "cpu_percent": cpu_percent,
                "memory_mb": memory_mb,
                "energy_joules": round(energy_joules, 2),
                "energy_kwh": round(energy_kwh, 6),
                "carbon_grams": round(carbon_grams, 4),
                "carbon_intensity": carbon_intensity,
            },
            "equivalents": {
                "smartphone_charges": round((carbon_grams * 1000) / 0.062, 1),
                "km_driven": round(carbon_grams / 192, 3),  # Auto promedio 192g/km
            },
        }

        # 5. Mostrar resultados
        self._print_results(result_data, output, success)

        # 6. Guardar historial
        if save_history:
            self._save_to_history(result_data)

        return result_data

    def _print_results(self, data: dict, output: str, success: bool):
        """Imprime resultados formateados"""
        m = data["metrics"]
        eq = data["equivalents"]

        print("\n" + "=" * 60)
        print("📊 RESULTADOS")
        print("=" * 60)

        # Status
        status_emoji = "✅" if success else "❌"
        print(f"\n{status_emoji} Estado: {'Exitoso' if success else 'Fallido'}")
        print(f"⏱️  Duración: {data['duration_seconds']} segundos")

        # Métricas de recursos
        print(f"\n🖥️  Recursos:")
        print(f"   CPU:    {m['cpu_percent']:.1f}%")
        print(f"   RAM:    {m['memory_mb']:.0f} MB")

        # Métricas de energía
        print(f"\n⚡ Energía:")
        print(f"   Consumo:  {m['energy_joules']:.2f} joules")
        print(f"   kWh:      {m['energy_kwh']:.6f}")

        # Carbono
        print(f"\n🌍 Emisiones:")
        print(f"   CO2e:     {m['carbon_grams']:.4f} gramos")
        print(f"   Grid:     {m['carbon_intensity']} g/kWh ({data['location']})")

        # Equivalencias
        print(f"\n💡 Equivalente a:")
        print(f"   📱 {eq['smartphone_charges']:.1f} cargas de smartphone")
        print(f"   🚗 {eq['km_driven']:.3f} km en auto")

        # Output del comando (resumido)
        if output:
            print(f"\n📝 Output (últimas 5 líneas):")
            lines = output.strip().split("\n")[-5:]
            for line in lines:
                print(f"   {line[:70]}")

        print("=" * 60)

    def _save_to_history(self, data: dict):
        """Guarda ejecución en historial local"""
        history = []

        if self.results_file.exists():
            with open(self.results_file, "r") as f:
                history = json.load(f)

        history.append(data)

        # Mantener últimas 100 ejecuciones
        history = history[-100:]

        with open(self.results_file, "w") as f:
            json.dump(history, f, indent=2)

        print(f"💾 Guardado en: {self.results_file}")

    def show_history(self, limit: int = 10):
        """Muestra historial de ejecuciones"""
        if not self.results_file.exists():
            print("📭 No hay historial aún")
            return

        with open(self.results_file, "r") as f:
            history = json.load(f)

        print(f"\n📜 HISTORIAL (últimas {limit} ejecuciones)")
        print("=" * 80)

        for entry in history[-limit:]:
            timestamp = entry["timestamp"][:19]
            cmd = entry["command"][:30]
            duration = entry["duration_seconds"]
            carbon = entry["metrics"]["carbon_grams"]

            print(f"{timestamp} | {cmd:30} | {duration:5.1f}s | {carbon:8.4f}g CO2e")

        # Estadísticas totales
        total_carbon = sum(e["metrics"]["carbon_grams"] for e in history)
        total_energy = sum(e["metrics"]["energy_joules"] for e in history)

        print("=" * 80)
        print(f"📊 Total: {len(history)} ejecuciones")
        print(f"💨 Emisiones acumuladas: {total_carbon:.2f}g CO2e")
        print(f"⚡ Energía acumulada: {total_energy:.0f} joules")
        print(
            f"📱 Equivalente a: {(total_carbon * 1000 / 0.062):.0f} cargas de smartphone"
        )

    def compare_locations(self, command: str):
        """Compara el mismo comando en diferentes ubicaciones"""
        locations = [
            ("Colombia", "CO"),
            ("Alemania", "DE"),
            ("California", "US-CA"),
            ("Francia", "FR"),
        ]

        print(f"\n🌍 COMPARACIÓN POR UBICACIÓN")
        print(f"Comando: {command}")
        print("=" * 80)

        results = []
        for name, code in locations:
            result = self.run_command(command, location=code, save_history=False)
            results.append((name, result))
            time.sleep(1)  # Pequeña pausa entre ejecuciones

        # Mostrar comparación
        print("\n📊 COMPARACIÓN DE EMISIONES:")
        print("=" * 80)

        baseline = results[0][1]["metrics"]["carbon_grams"]

        for name, result in results:
            carbon = result["metrics"]["carbon_grams"]
            diff_percent = ((carbon - baseline) / baseline) * 100
            diff_emoji = "📈" if diff_percent > 0 else "📉"

            print(
                f"{name:15} | {carbon:8.4f}g CO2e | {diff_emoji} {diff_percent:+6.1f}%"
            )


def main():
    """Punto de entrada del CLI"""
    parser = argparse.ArgumentParser(
        description="🌱 GreenPipeline - Mide la huella de carbono de tu código",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  greenpipeline run "npm test" --location CO
  greenpipeline run "python -m pytest" --location US-CA
  greenpipeline history
  greenpipeline compare "npm run build"
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")

    # Comando: run
    run_parser = subparsers.add_parser("run", help="Ejecutar comando con medición")
    run_parser.add_argument("cmd", help="Comando a ejecutar")
    run_parser.add_argument(
        "--location", "-l", default="GLOBAL", help="Ubicación (CO, US, DE, etc)"
    )

    # Comando: history
    subparsers.add_parser("history", help="Mostrar historial")

    # Comando: compare
    compare_parser = subparsers.add_parser(
        "compare", help="Comparar en diferentes ubicaciones"
    )
    compare_parser.add_argument("cmd", help="Comando a comparar")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = GreenPipelineCLI()

    if args.command == "run":
        cli.run_command(args.cmd, location=args.location)

    elif args.command == "history":
        cli.show_history()

    elif args.command == "compare":
        cli.compare_locations(args.cmd)

