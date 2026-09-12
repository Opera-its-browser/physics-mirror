import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox

# Начальные параметры
R_init = 4.00
a_init = 3.00
current_type = 'Вогнутое'

fig, ax = plt.subplots(figsize=(11, 6.5))
plt.subplots_adjust(left=0.1, bottom=0.38)

# Функция отрисовки схемы
def update_plot(mirror_type, a, R):
    ax.clear()
    ax.axhline(0, color='black', linestyle='--', linewidth=1, label='Оптическая ось')
    
    F_val = R / 2.0
    
    # 1. Положение элементов в зависимости от типа зеркала (зеркало в x = 0)
    if mirror_type == 'Вогнутое':
        F = -F_val  # Фокус слева
        C = -R      # Центр кривизны слева
        
        theta = np.linspace(-np.pi/6, np.pi/6, 100)
        xs = R * (np.cos(theta) - 1)
        ys = R * np.sin(theta)
        ax.plot(xs, ys, color='grey', linewidth=4)
        ax.plot(xs + 0.1, ys, color='darkgrey', linestyle=':', linewidth=1)
    else:  # Выпуклое
        F = F_val   # Фокус справа
        C = R       # Центр кривизны справа
        
        theta = np.linspace(-np.pi/6, np.pi/6, 100)
        xs = -R * (np.cos(theta) - 1)
        ys = R * np.sin(theta)
        ax.plot(xs, ys, color='grey', linewidth=4)
        ax.plot(xs - 0.1, ys, color='darkgrey', linestyle=':', linewidth=1)

    # Точки F и C
    ax.plot(F, 0, 'go', label=f'Фокус F ({F:.2f})')
    ax.plot(C, 0, 'bo', label=f'Центр C ({C:.2f})')
    ax.text(F, 0.25, f'F\n({F:.2f})', color='green', fontsize=10, ha='center')
    ax.text(C, 0.25, f'C\n({C:.2f})', color='blue', fontsize=10, ha='center')

    # Источник (S) - слева на расстоянии a
    S_x = -a
    S_y = 0.0
    ax.plot(S_x, S_y, 'ro', markersize=8, label=f'Источник S (-{a:.2f})')
    ax.text(S_x, 0.35, f'S ({S_x:.2f})', color='red', fontsize=12, ha='center', weight='bold')

    # 2. Расчет положения изображения S'
    f_val = F_val if mirror_type == 'Вогнутое' else -F_val
    
    if abs(a - f_val) < 1e-4:
        S_prime_x = None
        ax.text(0, -1.8, "Изображение в бесконечности (а = F)", 
                color='purple', fontsize=12, ha='center', weight='bold')
    else:
        b = 1.0 / (1.0 / f_val - 1.0 / a)
        S_prime_x = -b if mirror_type == 'Вогнутое' else b
        
        img_color = 'purple'
        img_type_str = 'Действительное' if S_prime_x < 0 else 'Мнимое'
        ax.plot(S_prime_x, 0, 'o', color=img_color, markersize=8, 
                label=f"Изображение S' ({S_prime_x:.2f}, {img_type_str})")
        ax.text(S_prime_x, -0.45, f"S'\n({S_prime_x:.2f})", color=img_color, 
                fontsize=11, ha='center', weight='bold')

    # 3. Отрисовка лучей
    H_y = 1.0
    H_x = 0.0

    ax.plot([S_x, H_x], [S_y, H_y], color="orange", lw=1.5, label="Падающий луч")
    ax.annotate('', xy=(H_x, H_y), xytext=(S_x, S_y),
                arrowprops=dict(arrowstyle="->", color="orange", lw=1.5))

    if mirror_type == 'Вогнутое':
        if a > F_val:  # Действительное изображение
            if S_prime_x is not None:
                dx = S_prime_x - H_x
                dy = 0.0 - H_y
                ax.plot([H_x, S_prime_x + dx * 0.5], [H_y, 0.0 + dy * 0.5], color="red", label="Отраженный луч")
                ax.annotate('', xy=(S_prime_x, 0), xytext=(H_x, H_y),
                            arrowprops=dict(arrowstyle="->", color="red", lw=1.5))
        else:  # Мнимое изображение (a < F_val)
            if S_prime_x is not None:
                dx = H_x - S_prime_x
                dy = H_y - 0.0
                ax.plot([H_x, H_x - dx * 0.8], [H_y, H_y + dy * 0.8], color="red", label="Отраженный луч")
                ax.plot([H_x, S_prime_x], [H_y, 0], 'r--', alpha=0.7, label="Продолжение (мнимое)")
    else:  # Выпуклое зеркало
        if S_prime_x is not None:
            dx = H_x - S_prime_x
            dy = H_y - 0.0
            ax.plot([H_x, H_x + dx * 0.8], [H_y, H_y + dy * 0.8], color="red", label="Отраженный луч")
            ax.plot([H_x, S_prime_x], [H_y, 0], 'r--', alpha=0.7, label="Продолжение (мнимое)")

    # Настройки осей
    ax.set_xlim(-10, 10)
    ax.set_ylim(-3.5, 3.5)
    ax.set_aspect('equal')
    ax.set_title(f"Сферическое зеркало ({mirror_type.lower()}е) | R = {R:.2f}, F = {F_val:.2f}, a = {a:.2f}", fontsize=13)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper left', fontsize=8)
    fig.canvas.draw_idle()

# --- Элементы управления ---

# 1. Слайдер и TextBox для расстояния a
ax_slider_a = plt.axes([0.20, 0.20, 0.45, 0.03])
slider_a = Slider(ax_slider_a, 'Расстояние a', 0.10, 9.50, valinit=a_init, valstep=0.01, valfmt='%.2f')

ax_box_a = plt.axes([0.67, 0.20, 0.08, 0.03])
text_box_a = TextBox(ax_box_a, '', initial=f"{a_init:.2f}")

# 2. Слайдер и TextBox для радиуса R
ax_slider_r = plt.axes([0.20, 0.13, 0.45, 0.03])
slider_r = Slider(ax_slider_r, 'Радиус R', 1.00, 10.00, valinit=R_init, valstep=0.01, valfmt='%.2f')

ax_box_r = plt.axes([0.67, 0.13, 0.08, 0.03])
text_box_r = TextBox(ax_box_r, '', initial=f"{R_init:.2f}")

# 3. Кнопка переключения типа зеркала (вместо RadioButtons)
ax_button = plt.axes([0.78, 0.15, 0.18, 0.06])
btn_type = Button(ax_button, 'Тип: Вогнутое', color='lightgray', hovercolor='0.9')

is_updating = False

def sync_and_update(source_type):
    global is_updating, current_type
    if is_updating:
        return
    is_updating = True

    try:
        if source_type == 'slider_a':
            text_box_a.set_val(f"{slider_a.val:.2f}")
        elif source_type == 'box_a':
            val = float(text_box_a.text.replace(',', '.'))
            val = np.clip(val, slider_a.valmin, slider_a.valmax)
            slider_a.set_val(val)
        elif source_type == 'slider_r':
            text_box_r.set_val(f"{slider_r.val:.2f}")
        elif source_type == 'box_r':
            val = float(text_box_r.text.replace(',', '.'))
            val = np.clip(val, slider_r.valmin, slider_r.valmax)
            slider_r.set_val(val)
        elif source_type == 'button':
            current_type = 'Выпуклое' if current_type == 'Вогнутое' else 'Вогнутое'
            btn_type.label.set_text(f'Тип: {current_type}')
    except ValueError:
        pass

    update_plot(current_type, slider_a.val, slider_r.val)
    is_updating = False

# Привязка событий
slider_a.on_changed(lambda val: sync_and_update('slider_a'))
text_box_a.on_submit(lambda val: sync_and_update('box_a'))

slider_r.on_changed(lambda val: sync_and_update('slider_r'))
text_box_r.on_submit(lambda val: sync_and_update('box_r'))

btn_type.on_clicked(lambda event: sync_and_update('button'))

# Первый запуск
update_plot(current_type, a_init, R_init)
plt.show()
