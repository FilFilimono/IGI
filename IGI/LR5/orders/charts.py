"""Графики статистики на matplotlib (без JavaScript)."""
import base64
import io

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'DejaVu Sans'


def _fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('ascii')


def monthly_trend_chart(labels, values, trend):
    """Линейный график продаж и тренда."""
    if not labels:
        return None
    fig, ax = plt.subplots(figsize=(8, 3.5))
    x = list(range(len(labels)))
    sales = [v if v is not None else float('nan') for v in values]
    ax.plot(x, sales, 'o-', color='#0d6efd', label='Продажи (руб.)', linewidth=2, markersize=5)
    if trend:
        ax.plot(x[:len(trend)], trend, '--', color='#dc3545', label='Тренд / прогноз', linewidth=2)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha='right', fontsize=8)
    ax.set_ylabel('руб.')
    ax.legend(loc='upper left', fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_title('Ежемесячный объём + тренд')
    fig.tight_layout()
    return _fig_to_base64(fig)


def city_bar_chart(labels, values):
    """Столбчатая диаграмма клиентов по городам."""
    if not labels:
        return None
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.bar(labels, values, color='#0d6efd')
    ax.set_ylabel('Клиентов')
    ax.set_title('Клиенты по городам')
    ax.tick_params(axis='x', rotation=35, labelsize=8)
    ax.grid(axis='y', alpha=0.3)
    fig.tight_layout()
    return _fig_to_base64(fig)
