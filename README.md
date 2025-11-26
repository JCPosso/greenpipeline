# 🌱 GreenPipeline Framework

**Mide, visualiza y optimiza la huella de carbono de tu software desde el desarrollo.**

## ¿Qué es GreenPipeline?

GreenPipeline es un framework open-source que se integra en tu pipeline CI/CD para:

- ⚡ **Medir** el consumo energético de cada build en tiempo real
- 🌍 **Calcular** las emisiones de CO2 basándose en la intensidad de carbono del grid eléctrico
- 📊 **Visualizar** métricas en dashboards y comentarios automáticos en PRs
- 🎯 **Optimizar** con sugerencias accionables y carbon-aware scheduling

## 🚀 Instalación Rápida

```bash
# Instalar desde PyPI
pip install greenpipeline

# O desde el código fuente
git clone https://github.com/greenpipeline
pip install -e .
```

## 💻 Uso CLI

```bash
# Medir un comando
greenpipeline run "npm test" --location CO

# Ver historial
greenpipeline history

# Comparar ubicaciones
greenpipeline compare "npm run build"
```

## 🔌 Integración GitHub Actions

```yaml
# .github/workflows/ci.yml
steps:
  - name: Start GreenPipeline
    uses: greenpipeline/action@v1
    with:
      mode: start
      location: CO

  # ... tus steps normales ...

  - name: GreenPipeline Report
    uses: greenpipeline/action@v1
    with:
      mode: report
      comment-pr: true
```

## 📊 Ejemplo de Output

```
🌱 GREENPIPELINE REPORT
============================================================
⏱️  Duración:     45.2 segundos
⚡ Energía:      1130.50 joules
🌍 Emisiones:    0.0532g CO2e
📊 SCI Score:    0.0532
📍 Ubicación:    CO (165g/kWh)

💡 Equivalente a: 0.9 cargas de smartphone
============================================================
```

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                   CI/CD Pipeline                    │
│  (GitHub Actions / GitLab CI / Jenkins)             │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────▼──────────┐
         │  GreenPipeline Core  │
         │   - Energy Estimator │
         │   - Carbon API       │
         │   - SCI Calculator   │
         └───────────┬──────────┘
                     │
      ┌──────────────┼──────────────┐
      │              │              │
┌─────▼────┐  ┌─────▼────┐  ┌─────▼────┐
│  Kepler  │  │ EcoCI ML │  │ Cloud    │
│  (CNCF)  │  │ Models   │  │ APIs     │
└──────────┘  └──────────┘  └──────────┘
```

## 🎯 Casos de Uso

### 1. Medición Continua
Integra en tu CI/CD y obtén métricas de carbono en cada commit.

### 2. Optimización de Código
Detecta código ineficiente que consume más energía de la necesaria.

### 3. Carbon-Aware Scheduling
Ejecuta builds cuando el grid eléctrico tiene más energía renovable.

### 4. Reporting ESG
Genera reportes de sostenibilidad para cumplimiento corporativo.

## 📚 Tecnologías Base

- **[Kepler](https://github.com/sustainable-computing-io/kepler)** (CNCF) - Medición a nivel de contenedor
- **[EcoCI](https://github.com/green-coding-solutions/eco-ci-energy-estimation)** - Modelos ML de estimación
- **[Carbon Aware SDK](https://github.com/Green-Software-Foundation/carbon-aware-sdk)** - Intensidad de carbono en tiempo real
- **[SCI Standard](https://sci.greensoftware.foundation/)** - Especificación ISO para Software Carbon Intensity

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para más detalles.

## 🌟 Roadmap

- [x] MVP - Medición básica de energía
- [x] CLI tool
- [x] GitHub Actions plugin
- [ ] GitLab CI integration
- [ ] Dashboard web con Grafana
- [ ] Detección automática de ineficiencias con ML
- [ ] Carbon-aware scheduling automático
- [ ] Integración con Prometheus/OpenTelemetry

## 📞 Contacto

- Website: https://greenpipeline.dev
- Twitter: @greenpipeline
- Email: hello@greenpipeline.dev

---

Hecho con 💚 por Juan Camilo Posso G.