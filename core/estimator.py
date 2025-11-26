import psutil
import time
import platform
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class EnergyMetrics:
    """Métricas de energía medidas"""

    duration_seconds: float
    cpu_percent: float
    memory_mb: float
    energy_joules: float
    carbon_grams: float
    sci_score: float


class EnergyEstimator:
    """
    Estima consumo energético basado en métricas del sistema.
    Usa coeficientes de SPECpower y modelos ML simplificados.
    """

    # Coeficientes TDP promedio por tipo de CPU (Watts)
    CPU_TDP = {
        "x86_64": 65,  # Intel/AMD típico
        "aarch64": 15,  # ARM (M1/M2)
        "arm64": 15,
    }

    # Factor de conversión CPU% -> Potencia (basado en estudios EcoCI)
    # Potencia = TDP * (CPU_util * 0.6 + 0.4)  # Modelo lineal con baseline
    CPU_POWER_FACTOR = 0.6
    CPU_BASELINE = 0.4

    # RAM: ~0.375W por GB (estudios Kingston/Crucial)
    RAM_WATTS_PER_GB = 0.375

    def __init__(self, carbon_intensity: float = 475):
        """
        Args:
            carbon_intensity: g CO2e por kWh (default: promedio global)
        """
        self.carbon_intensity = carbon_intensity
        self.platform = platform.machine().lower()
        self.tdp = self.CPU_TDP.get(self.platform, 65)

    def measure_execution(self, func, *args, **kwargs):
        """
        Mide el consumo energético de una función durante su ejecución.

        Returns:
            tuple: (resultado_funcion, EnergyMetrics)
        """
        # Mediciones iniciales
        cpu_samples = []
        memory_samples = []
        start_time = time.time()

        # Muestreo durante ejecución (cada 0.1s)
        def sample_metrics():
            while getattr(sample_metrics, "running", True):
                cpu_samples.append(psutil.cpu_percent(interval=0.1))
                memory_samples.append(psutil.virtual_memory().used / (1024**3))  # GB
                time.sleep(0.1)

        # Thread para muestreo paralelo
        import threading

        sample_thread = threading.Thread(target=sample_metrics, daemon=True)
        sample_thread.start()

        try:
            # Ejecutar función
            result = func(*args, **kwargs)
        finally:
            sample_metrics.running = False
            sample_thread.join(timeout=1)

        duration = time.time() - start_time

        # Calcular promedios
        avg_cpu = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0
        avg_memory_gb = (
            sum(memory_samples) / len(memory_samples) if memory_samples else 0
        )

        # Calcular energía
        metrics = self._calculate_energy(duration, avg_cpu, avg_memory_gb)

        return result, metrics

    def _calculate_energy(
        self, duration: float, cpu_percent: float, memory_gb: float
    ) -> EnergyMetrics:
        """
        Calcula energía usando modelo de potencia.

        Modelo:
        P_cpu = TDP * (CPU_util * 0.6 + 0.4)
        P_ram = RAM_GB * 0.375W
        E = (P_cpu + P_ram) * duration
        """
        # Normalizar CPU% (0-100 -> 0-1)
        cpu_util = cpu_percent / 100.0

        # Potencia CPU (watts)
        cpu_power = self.tdp * (cpu_util * self.CPU_POWER_FACTOR + self.CPU_BASELINE)

        # Potencia RAM (watts)
        ram_power = memory_gb * self.RAM_WATTS_PER_GB

        # Potencia total
        total_power_watts = cpu_power + ram_power

        # Energía (joules) = Power(W) * time(s)
        energy_joules = total_power_watts * duration

        # Energía (kWh)
        energy_kwh = energy_joules / 3600000

        # Carbono (gramos CO2e)
        carbon_grams = energy_kwh * self.carbon_intensity

        # SCI Score simplificado (g CO2e por ejecución)
        sci_score = carbon_grams

        return EnergyMetrics(
            duration_seconds=duration,
            cpu_percent=cpu_percent,
            memory_mb=memory_gb * 1024,
            energy_joules=energy_joules,
            carbon_grams=carbon_grams,
            sci_score=sci_score,
        )

    def estimate_from_metrics(
        self, duration: float, cpu_percent: float, memory_mb: float
    ) -> EnergyMetrics:
        """
        Estima energía desde métricas ya capturadas.
        Útil para integración con CI/CD que ya tiene métricas.
        """
        return self._calculate_energy(duration, cpu_percent, memory_mb / 1024)


# Ejemplo de uso
if __name__ == "__main__":
    # Test con función simple
    def heavy_computation():
        """Simula carga computacional"""
        result = sum([i**2 for i in range(10_000_000)])
        return result

    estimator = EnergyEstimator(carbon_intensity=420)  # Alemania promedio

    print("🌱 GreenPipeline Energy Estimator")
    print("=" * 50)
    print(f"Platform: {estimator.platform}")
    print(f"CPU TDP: {estimator.tdp}W")
    print(f"Carbon Intensity: {estimator.carbon_intensity}g CO2e/kWh")
    print("=" * 50)
    print("\n⚡ Midiendo ejecución...\n")

    result, metrics = estimator.measure_execution(heavy_computation)

    print("📊 Resultados:")
    print(f"  Duración:     {metrics.duration_seconds:.2f} segundos")
    print(f"  CPU promedio: {metrics.cpu_percent:.1f}%")
    print(f"  RAM promedio: {metrics.memory_mb:.0f} MB")
    print(f"  Energía:      {metrics.energy_joules:.2f} joules")
    print(f"  Carbono:      {metrics.carbon_grams:.4f} g CO2e")
    print(f"  SCI Score:    {metrics.sci_score:.4f}")
    print(
        f"\n💡 Equivalente a: {(metrics.carbon_grams * 1000 / 0.062):.0f} cargas de smartphone"
    )
