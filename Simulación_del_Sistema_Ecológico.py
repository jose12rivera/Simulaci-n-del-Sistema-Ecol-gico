import tkinter as tk
from tkinter import ttk, messagebox
import math

class EcosystemSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("🦊 Simulador de Ecosistema - Parque Nacional")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f0f9ff")
        
        # Parámetros iniciales
        self.params = {
            'foxes_init': 10,
            'rabbits_init': 50,
            'carrots_init': 200,
            'rabbits_per_fox_per_day': 0.5,
            'carrots_per_rabbit_per_day': 2.0,
            'carrot_growth_rate': 15,
            'fox_death_rate': 0.05,
            'rabbit_death_rate': 0.03,
            'rabbit_birth_rate': 0.1,
            'max_carrots': 500
        }
        
        # Estado de la simulación
        self.reset_simulation()
        self.is_running = False
        self.animation_speed = 200  # milisegundos
        
        self.create_widgets()
        self.update_display()
        
    def reset_simulation(self):
        self.day = 0
        self.foxes = float(self.params['foxes_init'])
        self.rabbits = float(self.params['rabbits_init'])
        self.carrots = float(self.params['carrots_init'])
        self.history = {
            'day': [],
            'foxes': [],
            'rabbits': [],
            'carrots': []
        }
        
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f0f9ff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Frame de alertas
        self.alert_frame = tk.Frame(main_frame, bg="#fee2e2", relief=tk.RIDGE, bd=2)
        self.alert_label = tk.Label(self.alert_frame, text="", bg="#fee2e2", 
                                    fg="#991b1b", font=("Arial", 10, "bold"), 
                                    justify=tk.LEFT, wraplength=1300)
        self.alert_label.pack(padx=10, pady=10)
        
        # Frame de estadísticas
        stats_frame = tk.Frame(main_frame, bg="#f0f9ff")
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.create_stat_cards(stats_frame)
        
        # Frame de configuración
        self.config_frame = tk.Frame(main_frame, bg="white", relief=tk.RIDGE, bd=2)
        self.create_config_panel()
        
        # Frame del gráfico
        graph_frame = tk.Frame(main_frame, bg="white", relief=tk.RIDGE, bd=2)
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.create_graph_canvas(graph_frame)
        
        # Frame de análisis
        self.analysis_frame = tk.Frame(main_frame, bg="white", relief=tk.RIDGE, bd=2)
        self.analysis_frame.pack(fill=tk.X, pady=10)
        
        analysis_title = tk.Label(self.analysis_frame, text="💡 Análisis y Recomendaciones", 
                                 bg="white", fg="#1f2937", font=("Arial", 14, "bold"))
        analysis_title.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        self.analysis_text = tk.Text(self.analysis_frame, height=6, wrap=tk.WORD, 
                                    font=("Arial", 10), relief=tk.FLAT, bg="#f9fafb")
        self.analysis_text.pack(fill=tk.X, padx=15, pady=(0, 10))
        
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg="white", relief=tk.RIDGE, bd=2)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Título y día
        title_frame = tk.Frame(header_frame, bg="white")
        title_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        title_label = tk.Label(title_frame, text="🦊 Simulador de Ecosistema - Parque Nacional", 
                              bg="white", fg="#1f2937", font=("Arial", 18, "bold"))
        title_label.pack(anchor=tk.W)
        
        self.day_label = tk.Label(title_frame, text="Día: 0", 
                                 bg="white", fg="#2563eb", font=("Arial", 12, "bold"))
        self.day_label.pack(anchor=tk.W)
        
        # Botones
        button_frame = tk.Frame(header_frame, bg="white")
        button_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        self.play_button = tk.Button(button_frame, text="▶ Iniciar", 
                                     command=self.toggle_simulation,
                                     bg="#22c55e", fg="white", font=("Arial", 11, "bold"),
                                     padx=20, pady=8, cursor="hand2", relief=tk.FLAT)
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        reset_button = tk.Button(button_frame, text="↻ Reiniciar", 
                                command=self.reset_button_click,
                                bg="#6b7280", fg="white", font=("Arial", 11, "bold"),
                                padx=20, pady=8, cursor="hand2", relief=tk.FLAT)
        reset_button.pack(side=tk.LEFT, padx=5)
        
        self.config_button = tk.Button(button_frame, text="⚙ Configurar", 
                                       command=self.toggle_config,
                                       bg="#3b82f6", fg="white", font=("Arial", 11, "bold"),
                                       padx=20, pady=8, cursor="hand2", relief=tk.FLAT)
        self.config_button.pack(side=tk.LEFT, padx=5)
        
    def create_stat_cards(self, parent):
        # Tarjeta Zorros
        fox_frame = tk.Frame(parent, bg="#f97316", relief=tk.RIDGE, bd=0)
        fox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(fox_frame, text="🦊 Zorros", bg="#f97316", fg="white", 
                font=("Arial", 14, "bold")).pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        self.fox_value = tk.Label(fox_frame, text="10.0", bg="#f97316", fg="white", 
                                 font=("Arial", 32, "bold"))
        self.fox_value.pack(anchor=tk.W, padx=20)
        
        self.fox_initial = tk.Label(fox_frame, text=f"Inicial: {self.params['foxes_init']}", 
                                   bg="#f97316", fg="white", font=("Arial", 9))
        self.fox_initial.pack(anchor=tk.W, padx=20, pady=(0, 15))
        
        # Tarjeta Conejos
        rabbit_frame = tk.Frame(parent, bg="#6b7280", relief=tk.RIDGE, bd=0)
        rabbit_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(rabbit_frame, text="🐰 Conejos", bg="#6b7280", fg="white", 
                font=("Arial", 14, "bold")).pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        self.rabbit_value = tk.Label(rabbit_frame, text="50.0", bg="#6b7280", fg="white", 
                                     font=("Arial", 32, "bold"))
        self.rabbit_value.pack(anchor=tk.W, padx=20)
        
        self.rabbit_initial = tk.Label(rabbit_frame, text=f"Inicial: {self.params['rabbits_init']}", 
                                      bg="#6b7280", fg="white", font=("Arial", 9))
        self.rabbit_initial.pack(anchor=tk.W, padx=20, pady=(0, 15))
        
        # Tarjeta Zanahorias
        carrot_frame = tk.Frame(parent, bg="#fb923c", relief=tk.RIDGE, bd=0)
        carrot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(carrot_frame, text="🥕 Zanahorias", bg="#fb923c", fg="white", 
                font=("Arial", 14, "bold")).pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        self.carrot_value = tk.Label(carrot_frame, text="200", bg="#fb923c", fg="white", 
                                     font=("Arial", 32, "bold"))
        self.carrot_value.pack(anchor=tk.W, padx=20)
        
        self.carrot_initial = tk.Label(carrot_frame, text=f"Inicial: {self.params['carrots_init']}", 
                                      bg="#fb923c", fg="white", font=("Arial", 9))
        self.carrot_initial.pack(anchor=tk.W, padx=20, pady=(0, 15))
        
    def create_config_panel(self):
        title = tk.Label(self.config_frame, text="⚙️ Configuración del Ecosistema", 
                        bg="white", fg="#1f2937", font=("Arial", 14, "bold"))
        title.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        # Grid de configuración
        grid_frame = tk.Frame(self.config_frame, bg="white")
        grid_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        configs = [
            ("Zorros iniciales:", 'foxes_init', 0),
            ("Conejos iniciales:", 'rabbits_init', 1),
            ("Zanahorias iniciales:", 'carrots_init', 2),
            ("Conejos/día por zorro:", 'rabbits_per_fox_per_day', 3),
            ("Zanahorias/día por conejo:", 'carrots_per_rabbit_per_day', 4),
            ("Crecimiento zanahorias (%):", 'carrot_growth_rate', 5),
        ]
        
        self.config_entries = {}
        
        for i, (label_text, key, col) in enumerate(configs):
            frame = tk.Frame(grid_frame, bg="white")
            frame.grid(row=0, column=col, padx=10, pady=5, sticky="ew")
            
            label = tk.Label(frame, text=label_text, bg="white", fg="#374151", 
                           font=("Arial", 9, "bold"))
            label.pack(anchor=tk.W)
            
            entry = tk.Entry(frame, font=("Arial", 10), relief=tk.SOLID, bd=1)
            entry.insert(0, str(self.params[key]))
            entry.pack(fill=tk.X)
            
            self.config_entries[key] = entry
        
        for col in range(6):
            grid_frame.columnconfigure(col, weight=1)
            
    def create_graph_canvas(self, parent):
        title = tk.Label(parent, text="📊 Evolución del Ecosistema (Canvas)", 
                        bg="white", fg="#1f2937", font=("Arial", 14, "bold"))
        title.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        # Crear canvas para el gráfico
        self.canvas_frame = tk.Frame(parent, bg="white")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        self.graph_canvas = tk.Canvas(self.canvas_frame, bg="white", highlightthickness=1, 
                                     highlightbackground="#d1d5db")
        self.graph_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Leyenda
        legend_frame = tk.Frame(self.canvas_frame, bg="white")
        legend_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(legend_frame, text="🦊 Zorros", fg="#f97316", bg="white", 
                font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=20)
        tk.Label(legend_frame, text="🐰 Conejos", fg="#6b7280", bg="white", 
                font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=20)
        tk.Label(legend_frame, text="🥕 Zanahorias", fg="#fb923c", bg="white", 
                font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=20)
        
    def draw_graph(self):
        if len(self.history['day']) < 2:
            return
            
        self.graph_canvas.delete("all")
        
        width = self.graph_canvas.winfo_width()
        height = self.graph_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
            
        padding = 50
        graph_width = width - 2 * padding
        graph_height = height - 2 * padding
        
        # Encontrar valores máximos para escalar
        max_foxes = max(self.history['foxes']) if self.history['foxes'] else 1
        max_rabbits = max(self.history['rabbits']) if self.history['rabbits'] else 1
        max_carrots = max(self.history['carrots']) if self.history['carrots'] else 1
        max_value = max(max_foxes, max_rabbits, max_carrots, 1)
        max_day = max(self.history['day']) if self.history['day'] else 1
        
        # Dibujar ejes
        self.graph_canvas.create_line(padding, height - padding, width - padding, height - padding, width=2)  # Eje X
        self.graph_canvas.create_line(padding, padding, padding, height - padding, width=2)  # Eje Y
        
        # Dibujar líneas de población
        points_foxes = []
        points_rabbits = []
        points_carrots = []
        
        for i, day in enumerate(self.history['day']):
            x = padding + (day / max_day) * graph_width if max_day > 0 else padding
            
            # Zorros
            y_fox = height - padding - (self.history['foxes'][i] / max_value) * graph_height
            points_foxes.extend([x, y_fox])
            
            # Conejos
            y_rab = height - padding - (self.history['rabbits'][i] / max_value) * graph_height
            points_rabbits.extend([x, y_rab])
            
            # Zanahorias
            y_car = height - padding - (self.history['carrots'][i] / max_value) * graph_height
            points_carrots.extend([x, y_car])
        
        # Dibujar las líneas
        if len(points_foxes) >= 4:
            self.graph_canvas.create_line(points_foxes, fill="#f97316", width=3, smooth=True)
        if len(points_rabbits) >= 4:
            self.graph_canvas.create_line(points_rabbits, fill="#6b7280", width=3, smooth=True)
        if len(points_carrots) >= 4:
            self.graph_canvas.create_line(points_carrots, fill="#fb923c", width=3, smooth=True)
        
        # Etiquetas
        self.graph_canvas.create_text(width // 2, height - 10, text="Días", font=("Arial", 10, "bold"))
        self.graph_canvas.create_text(15, height // 2, text="Población", angle=90, font=("Arial", 10, "bold"))
        
    def simulate_day(self):
        # Guardar estado actual en historial
        self.history['day'].append(self.day)
        self.history['foxes'].append(self.foxes)
        self.history['rabbits'].append(self.rabbits)
        self.history['carrots'].append(self.carrots)
        
        # Mantener solo últimos 100 días
        if len(self.history['day']) > 100:
            for key in self.history:
                self.history[key] = self.history[key][-100:]
        
        # Conejos comen zanahorias
        carrots_eaten = min(self.carrots, 
                           self.rabbits * self.params['carrots_per_rabbit_per_day'])
        self.carrots -= carrots_eaten
        
        # Zorros comen conejos
        rabbits_eaten = min(self.rabbits, 
                           self.foxes * self.params['rabbits_per_fox_per_day'])
        self.rabbits -= rabbits_eaten
        
        # Reproducción de zanahorias
        self.carrots = min(self.params['max_carrots'], 
                          self.carrots * (1 + self.params['carrot_growth_rate'] / 100))
        
        # Muerte de zorros por falta de comida
        if self.foxes > 0:
            fox_food_ratio = rabbits_eaten / (self.foxes * self.params['rabbits_per_fox_per_day'])
            if fox_food_ratio < 0.5:
                self.foxes *= (1 - self.params['fox_death_rate'] * (1 - fox_food_ratio * 2))
        
        # Muerte de conejos por falta de comida
        if self.rabbits > 0:
            rabbit_food_ratio = carrots_eaten / (self.rabbits * self.params['carrots_per_rabbit_per_day'])
            if rabbit_food_ratio < 0.5:
                self.rabbits *= (1 - self.params['rabbit_death_rate'] * (1 - rabbit_food_ratio * 2))
            
            # Reproducción de conejos
            if rabbit_food_ratio > 0.7:
                self.rabbits *= (1 + self.params['rabbit_birth_rate'] * rabbit_food_ratio)
        
        # Asegurar valores positivos
        self.foxes = max(0, round(self.foxes * 10) / 10)
        self.rabbits = max(0, round(self.rabbits * 10) / 10)
        self.carrots = max(0, round(self.carrots))
        
        self.day += 1
        
    def check_alerts(self):
        alerts = []
        
        if 0 < self.foxes < 3:
            alerts.append("⚠️ Población de zorros en peligro crítico")
        if 0 < self.rabbits < 10:
            alerts.append("⚠️ Población de conejos en peligro")
        if self.carrots < 50:
            alerts.append("⚠️ Escasez de zanahorias")
        if self.foxes == 0:
            alerts.append("💀 Los zorros se han extinguido")
        if self.rabbits == 0:
            alerts.append("💀 Los conejos se han extinguido")
            
        if alerts:
            self.alert_frame.pack(fill=tk.X, pady=(0, 10), before=self.config_frame.master.winfo_children()[2])
            self.alert_label.config(text="⚠️ ALERTAS DEL ECOSISTEMA:\n" + "\n".join(alerts))
        else:
            self.alert_frame.pack_forget()
            
    def update_analysis(self):
        self.analysis_text.delete(1.0, tk.END)
        
        recommendations = []
        
        fox_ratio = self.foxes / self.params['foxes_init']
        rabbit_ratio = self.rabbits / self.params['rabbits_init']
        
        if fox_ratio > 1.5:
            recommendations.append("🔴 CONTROL NECESARIO: La población de zorros ha aumentado significativamente. "
                                 "Se recomienda implementar un programa de reubicación.\n")
        
        if rabbit_ratio > 2:
            recommendations.append("🔴 CONTROL NECESARIO: Sobrepoblación de conejos detectada. "
                                 "Considere aumentar la población de zorros o implementar control poblacional.\n")
        
        if 0 < fox_ratio < 0.3:
            recommendations.append("🚨 INTERVENCIÓN URGENTE: Población de zorros en peligro crítico. "
                                 "Se requiere introducir nuevos ejemplares o reducir población de conejos.\n")
        
        if self.day > 10 and not recommendations:
            recommendations.append("✅ ECOSISTEMA ESTABLE: Las poblaciones se encuentran en equilibrio. "
                                 "No se requiere intervención en este momento.\n")
        
        for rec in recommendations:
            self.analysis_text.insert(tk.END, rec + "\n")
            
    def update_display(self):
        self.day_label.config(text=f"Día: {self.day}")
        self.fox_value.config(text=f"{self.foxes:.1f}")
        self.rabbit_value.config(text=f"{self.rabbits:.1f}")
        self.carrot_value.config(text=f"{int(self.carrots)}")
        
        self.check_alerts()
        self.draw_graph()
        self.update_analysis()
        
    def toggle_simulation(self):
        self.is_running = not self.is_running
        
        if self.is_running:
            self.play_button.config(text="⏸ Pausar", bg="#eab308")
            self.run_simulation()
        else:
            self.play_button.config(text="▶ Iniciar", bg="#22c55e")
            
    def run_simulation(self):
        if self.is_running:
            self.simulate_day()
            self.update_display()
            self.root.after(self.animation_speed, self.run_simulation)
            
    def reset_button_click(self):
        self.is_running = False
        self.play_button.config(text="▶ Iniciar", bg="#22c55e")
        
        # Actualizar parámetros desde las entradas
        try:
            for key, entry in self.config_entries.items():
                self.params[key] = float(entry.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
            return
            
        self.reset_simulation()
        self.update_display()
        
    def toggle_config(self):
        if self.config_frame.winfo_ismapped():
            self.config_frame.pack_forget()
            self.config_button.config(text="⚙ Mostrar Config")
        else:
            self.config_frame.pack(fill=tk.X, pady=10, after=self.alert_frame if self.alert_frame.winfo_ismapped() else self.root.winfo_children()[0].winfo_children()[2])
            self.config_button.config(text="⚙ Ocultar Config")

def main():
    root = tk.Tk()
    app = EcosystemSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()