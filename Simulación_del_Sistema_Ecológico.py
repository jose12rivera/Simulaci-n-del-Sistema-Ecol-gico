import tkinter as tk
from tkinter import ttk, messagebox
import math

class EcosystemSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("🦊 Simulador de Ecosistema - Parque Nacional")
        self.root.geometry("1600x1000")
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
        self.animation_speed = 200
        self.current_graph = "line"  # line, bar, pie
        
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
                                    justify=tk.LEFT, wraplength=1500)
        self.alert_label.pack(padx=10, pady=10)
        
        # Frame de estadísticas
        stats_frame = tk.Frame(main_frame, bg="#f0f9ff")
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.create_stat_cards(stats_frame)
        
        # Frame de configuración
        self.config_frame = tk.Frame(main_frame, bg="white", relief=tk.RIDGE, bd=2)
        self.create_config_panel()
        
        # Frame del gráfico con selector
        graph_container = tk.Frame(main_frame, bg="white", relief=tk.RIDGE, bd=2)
        graph_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Selector de tipo de gráfico
        selector_frame = tk.Frame(graph_container, bg="white")
        selector_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(selector_frame, text="📊 Tipo de Gráfico:", 
                bg="white", fg="#1f2937", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        
        btn_line = tk.Button(selector_frame, text="📈 Líneas", 
                            command=lambda: self.change_graph("line"),
                            bg="#3b82f6", fg="white", font=("Arial", 10, "bold"),
                            padx=15, pady=6, cursor="hand2", relief=tk.FLAT)
        btn_line.pack(side=tk.LEFT, padx=5)
        
        btn_bar = tk.Button(selector_frame, text="📊 Barras", 
                           command=lambda: self.change_graph("bar"),
                           bg="#8b5cf6", fg="white", font=("Arial", 10, "bold"),
                           padx=15, pady=6, cursor="hand2", relief=tk.FLAT)
        btn_bar.pack(side=tk.LEFT, padx=5)
        
        btn_pie = tk.Button(selector_frame, text="🥧 Pastel", 
                           command=lambda: self.change_graph("pie"),
                           bg="#ec4899", fg="white", font=("Arial", 10, "bold"),
                           padx=15, pady=6, cursor="hand2", relief=tk.FLAT)
        btn_pie.pack(side=tk.LEFT, padx=5)
        
        self.graph_buttons = {"line": btn_line, "bar": btn_bar, "pie": btn_pie}
        
        self.create_graph_canvas(graph_container)
        
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
                font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=20)
        tk.Label(legend_frame, text="🐰 Conejos", fg="#6b7280", bg="white", 
                font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=20)
        tk.Label(legend_frame, text="🥕 Zanahorias", fg="#fb923c", bg="white", 
                font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=20)
    
    def change_graph(self, graph_type):
        self.current_graph = graph_type
        
        # Actualizar estilos de botones
        for gtype, btn in self.graph_buttons.items():
            if gtype == graph_type:
                btn.config(relief=tk.SUNKEN, bg="#1e40af" if gtype == "line" else 
                          "#6d28d9" if gtype == "bar" else "#be185d")
            else:
                btn.config(relief=tk.FLAT, bg="#3b82f6" if gtype == "line" else 
                          "#8b5cf6" if gtype == "bar" else "#ec4899")
        
        self.draw_graph()
        
    def draw_graph(self):
        if self.current_graph == "line":
            self.draw_line_graph()
        elif self.current_graph == "bar":
            self.draw_bar_graph()
        elif self.current_graph == "pie":
            self.draw_pie_chart()
    
    def draw_line_graph(self):
        if len(self.history['day']) < 2:
            return
            
        self.graph_canvas.delete("all")
        
        width = self.graph_canvas.winfo_width()
        height = self.graph_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
            
        padding = 60
        graph_width = width - 2 * padding
        graph_height = height - 2 * padding
        
        # Encontrar valores máximos
        max_foxes = max(self.history['foxes']) if self.history['foxes'] else 1
        max_rabbits = max(self.history['rabbits']) if self.history['rabbits'] else 1
        max_carrots = max(self.history['carrots']) if self.history['carrots'] else 1
        max_value = max(max_foxes, max_rabbits, max_carrots, 1)
        max_day = max(self.history['day']) if self.history['day'] else 1
        
        # Dibujar grid de fondo
        for i in range(5):
            y = padding + (i * graph_height / 4)
            self.graph_canvas.create_line(padding, y, width - padding, y, 
                                         fill="#e5e7eb", width=1, dash=(2, 4))
            value = max_value * (1 - i / 4)
            self.graph_canvas.create_text(padding - 10, y, text=f"{value:.0f}", 
                                         anchor=tk.E, font=("Arial", 9), fill="#6b7280")
        
        # Dibujar ejes principales
        self.graph_canvas.create_line(padding, height - padding, width - padding, 
                                     height - padding, width=3, fill="#374151")
        self.graph_canvas.create_line(padding, padding, padding, height - padding, 
                                     width=3, fill="#374151")
        
        # Preparar puntos
        points_foxes = []
        points_rabbits = []
        points_carrots = []
        
        for i, day in enumerate(self.history['day']):
            x = padding + (day / max_day) * graph_width if max_day > 0 else padding
            
            y_fox = height - padding - (self.history['foxes'][i] / max_value) * graph_height
            points_foxes.extend([x, y_fox])
            
            y_rab = height - padding - (self.history['rabbits'][i] / max_value) * graph_height
            points_rabbits.extend([x, y_rab])
            
            y_car = height - padding - (self.history['carrots'][i] / max_value) * graph_height
            points_carrots.extend([x, y_car])
        
        # Dibujar áreas sombreadas (efecto gradiente)
        if len(points_carrots) >= 4:
            area_points = points_carrots.copy()
            area_points.extend([width - padding, height - padding, padding, height - padding])
            self.graph_canvas.create_polygon(area_points, fill="#fed7aa", outline="")
        
        if len(points_rabbits) >= 4:
            area_points = points_rabbits.copy()
            area_points.extend([width - padding, height - padding, padding, height - padding])
            self.graph_canvas.create_polygon(area_points, fill="#d1d5db", outline="")
        
        if len(points_foxes) >= 4:
            area_points = points_foxes.copy()
            area_points.extend([width - padding, height - padding, padding, height - padding])
            self.graph_canvas.create_polygon(area_points, fill="#fed7aa", outline="")
        
        # Dibujar las líneas principales
        if len(points_carrots) >= 4:
            self.graph_canvas.create_line(points_carrots, fill="#fb923c", width=4, 
                                         smooth=True, capstyle=tk.ROUND)
        if len(points_rabbits) >= 4:
            self.graph_canvas.create_line(points_rabbits, fill="#6b7280", width=4, 
                                         smooth=True, capstyle=tk.ROUND)
        if len(points_foxes) >= 4:
            self.graph_canvas.create_line(points_foxes, fill="#f97316", width=4, 
                                         smooth=True, capstyle=tk.ROUND)
        
        # Dibujar puntos destacados
        for i in range(0, len(points_foxes), 4):
            if i < len(points_foxes):
                x, y = points_foxes[i], points_foxes[i+1]
                self.graph_canvas.create_oval(x-4, y-4, x+4, y+4, fill="#f97316", 
                                             outline="white", width=2)
        
        # Etiquetas
        self.graph_canvas.create_text(width // 2, height - 20, text="Días", 
                                     font=("Arial", 12, "bold"), fill="#1f2937")
        self.graph_canvas.create_text(25, height // 2, text="Población", angle=90, 
                                     font=("Arial", 12, "bold"), fill="#1f2937")
    
    def draw_bar_graph(self):
        if len(self.history['day']) < 1:
            return
            
        self.graph_canvas.delete("all")
        
        width = self.graph_canvas.winfo_width()
        height = self.graph_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
            
        padding = 60
        graph_width = width - 2 * padding
        graph_height = height - 2 * padding
        
        # Tomar últimos 20 días
        days_to_show = min(20, len(self.history['day']))
        start_idx = len(self.history['day']) - days_to_show
        
        days = self.history['day'][start_idx:]
        foxes = self.history['foxes'][start_idx:]
        rabbits = self.history['rabbits'][start_idx:]
        carrots = self.history['carrots'][start_idx:]
        
        max_value = max(max(foxes), max(rabbits), max(carrots), 1)
        
        # Dibujar grid
        for i in range(5):
            y = padding + (i * graph_height / 4)
            self.graph_canvas.create_line(padding, y, width - padding, y, 
                                         fill="#e5e7eb", width=1, dash=(2, 4))
            value = max_value * (1 - i / 4)
            self.graph_canvas.create_text(padding - 10, y, text=f"{value:.0f}", 
                                         anchor=tk.E, font=("Arial", 9), fill="#6b7280")
        
        # Dibujar ejes
        self.graph_canvas.create_line(padding, height - padding, width - padding, 
                                     height - padding, width=3, fill="#374151")
        self.graph_canvas.create_line(padding, padding, padding, height - padding, 
                                     width=3, fill="#374151")
        
        # Calcular ancho de barras
        bar_group_width = graph_width / days_to_show
        bar_width = bar_group_width / 4
        
        for i in range(days_to_show):
            x = padding + (i * bar_group_width) + bar_group_width / 2
            
            # Zanahorias
            h_carrot = (carrots[i] / max_value) * graph_height
            x1 = x - bar_width * 1.5
            y1 = height - padding - h_carrot
            y2 = height - padding
            self.draw_3d_bar(x1, y1, x1 + bar_width, y2, "#fb923c", "#ea580c")
            
            # Conejos
            h_rabbit = (rabbits[i] / max_value) * graph_height
            x1 = x - bar_width * 0.5
            y1 = height - padding - h_rabbit
            self.draw_3d_bar(x1, y1, x1 + bar_width, y2, "#6b7280", "#4b5563")
            
            # Zorros
            h_fox = (foxes[i] / max_value) * graph_height
            x1 = x + bar_width * 0.5
            y1 = height - padding - h_fox
            self.draw_3d_bar(x1, y1, x1 + bar_width, y2, "#f97316", "#ea580c")
            
            # Etiqueta del día
            if i % 2 == 0:
                self.graph_canvas.create_text(x, height - padding + 15, 
                                             text=f"D{days[i]}", 
                                             font=("Arial", 8), fill="#6b7280")
        
        # Etiquetas
        self.graph_canvas.create_text(width // 2, height - 20, text="Días", 
                                     font=("Arial", 12, "bold"), fill="#1f2937")
        self.graph_canvas.create_text(25, height // 2, text="Población", angle=90, 
                                     font=("Arial", 12, "bold"), fill="#1f2937")
    
    def draw_3d_bar(self, x1, y1, x2, y2, color, dark_color):
        # Sombra - usar gris claro en lugar de transparencia
        self.graph_canvas.create_rectangle(x1 + 3, y1 + 3, x2 + 3, y2 + 3, 
                                          fill="#d1d5db", outline="")
        
        # Barra principal con gradiente simulado
        bar_height = y2 - y1
        steps = max(1, int(bar_height / 5))
        
        for i in range(steps):
            y_start = y1 + (i * bar_height / steps)
            y_end = y1 + ((i + 1) * bar_height / steps)
            
            # Alternar entre colores para simular gradiente
            if i % 2 == 0:
                self.graph_canvas.create_rectangle(x1, y_start, x2, y_end, 
                                                  fill=color, outline="")
            else:
                self.graph_canvas.create_rectangle(x1, y_start, x2, y_end, 
                                                  fill=dark_color, outline="")
        
        # Borde
        self.graph_canvas.create_rectangle(x1, y1, x2, y2, outline="white", width=2)
        
        # Brillo superior - usar gris muy claro
        self.graph_canvas.create_rectangle(x1, y1, x2, y1 + 5, 
                                          fill="#f8fafc", outline="")
    
    def draw_pie_chart(self):
        if self.foxes == 0 and self.rabbits == 0 and self.carrots == 0:
            return
            
        self.graph_canvas.delete("all")
        
        width = self.graph_canvas.winfo_width()
        height = self.graph_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Centro y radio del gráfico
        center_x = width // 2
        center_y = height // 2
        radius = min(width, height) // 3
        
        # Calcular totales
        total = self.foxes + self.rabbits + self.carrots
        if total == 0:
            return
        
        # Calcular ángulos
        fox_angle = (self.foxes / total) * 360
        rabbit_angle = (self.rabbits / total) * 360
        carrot_angle = (self.carrots / total) * 360
        
        # Dibujar título
        self.graph_canvas.create_text(center_x, 30, 
                                     text="Distribución Actual del Ecosistema", 
                                     font=("Arial", 16, "bold"), fill="#1f2937")
        
        # Ángulo de inicio
        start_angle = 0
        
        # Lista de segmentos
        segments = [
            (fox_angle, "#f97316", "#ea580c", "🦊 Zorros", self.foxes),
            (rabbit_angle, "#6b7280", "#4b5563", "🐰 Conejos", self.rabbits),
            (carrot_angle, "#fb923c", "#ea580c", "🥕 Zanahorias", self.carrots)
        ]
        
        # Dibujar sombra - usar gris claro
        self.graph_canvas.create_oval(center_x - radius + 5, center_y - radius + 5,
                                     center_x + radius + 5, center_y + radius + 5,
                                     fill="#e5e7eb", outline="")
        
        # Dibujar segmentos
        for angle, color, dark_color, label, value in segments:
            if angle > 0:
                # Segmento principal
                self.graph_canvas.create_arc(center_x - radius, center_y - radius,
                                            center_x + radius, center_y + radius,
                                            start=start_angle, extent=angle,
                                            fill=color, outline="white", width=3)
                
                # Efecto 3D (borde oscuro)
                self.graph_canvas.create_arc(center_x - radius + 2, center_y - radius + 2,
                                            center_x + radius - 2, center_y + radius - 2,
                                            start=start_angle, extent=angle,
                                            fill=dark_color, outline="", width=0,
                                            style=tk.CHORD)
                
                # Calcular posición para etiqueta
                mid_angle = start_angle + angle / 2
                label_distance = radius * 0.7
                label_x = center_x + label_distance * math.cos(math.radians(mid_angle))
                label_y = center_y - label_distance * math.sin(math.radians(mid_angle))
                
                # Porcentaje
                percentage = (value / total) * 100
                
                # Dibujar etiqueta con fondo
                text = f"{percentage:.1f}%"
                self.graph_canvas.create_oval(label_x - 30, label_y - 20,
                                            label_x + 30, label_y + 20,
                                            fill="white", outline=color, width=2)
                self.graph_canvas.create_text(label_x, label_y, text=text,
                                            font=("Arial", 11, "bold"), fill=color)
                
                start_angle += angle
        
        # Círculo central para efecto donut
        inner_radius = radius * 0.4
        self.graph_canvas.create_oval(center_x - inner_radius, center_y - inner_radius,
                                     center_x + inner_radius, center_y + inner_radius,
                                     fill="white", outline="#e5e7eb", width=2)
        
        # Texto central
        self.graph_canvas.create_text(center_x, center_y - 10, text="Total",
                                     font=("Arial", 12, "bold"), fill="#6b7280")
        self.graph_canvas.create_text(center_x, center_y + 15, text=f"{int(total)}",
                                     font=("Arial", 20, "bold"), fill="#1f2937")
        
        # Leyenda detallada
        legend_y = height - 100
        legend_x_start = 50
        
        for i, (angle, color, dark_color, label, value) in enumerate(segments):
            x = legend_x_start + (i * (width - 100) // 3)
            
            # Cuadro de color
            self.graph_canvas.create_rectangle(x, legend_y, x + 30, legend_y + 30,
                                             fill=color, outline="white", width=2)
            
            # Texto
            self.graph_canvas.create_text(x + 40, legend_y + 5, text=label,
                                         anchor=tk.W, font=("Arial", 11, "bold"),
                                         fill=color)
            
            percentage = (value / total) * 100
            self.graph_canvas.create_text(x + 40, legend_y + 22,
                                         text=f"{value:.1f} ({percentage:.1f}%)",
                                         anchor=tk.W, font=("Arial", 9),
                                         fill="#6b7280")
    
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
            self.root.after(self.animation_speed, self.run_simulation)
    
    def simulate_day(self):
        # Guardar estado actual
        self.history['day'].append(self.day)
        self.history['foxes'].append(self.foxes)
        self.history['rabbits'].append(self.rabbits)
        self.history['carrots'].append(self.carrots)
        
        # Calcular cambios
        # 1. Zorros comen conejos
        rabbits_eaten = min(self.rabbits, self.foxes * self.params['rabbits_per_fox_per_day'])
        
        # 2. Conejos comen zanahorias
        carrots_eaten = min(self.carrots, self.rabbits * self.params['carrots_per_rabbit_per_day'])
        
        # 3. Actualizar poblaciones
        # Zorros: mueren por tasa de muerte, pero crecen si hay comida
        fox_survival = max(0, rabbits_eaten - self.foxes * self.params['fox_death_rate'])
        self.foxes = max(0, self.foxes - self.foxes * self.params['fox_death_rate'] + fox_survival * 0.1)
        
        # Conejos: mueren por depredación y tasa de muerte, pero se reproducen
        self.rabbits = max(0, self.rabbits - rabbits_eaten + 
                          self.rabbits * self.params['rabbit_birth_rate'] - 
                          self.rabbits * self.params['rabbit_death_rate'])
        
        # Zanahorias: son comidas pero crecen
        self.carrots = max(0, self.carrots - carrots_eaten + 
                          self.carrots * (self.params['carrot_growth_rate'] / 100))
        self.carrots = min(self.carrots, self.params['max_carrots'])
        
        self.day += 1
        self.update_display()
    
    def update_display(self):
        # Actualizar día
        self.day_label.config(text=f"Día: {self.day}")
        
        # Actualizar valores
        self.fox_value.config(text=f"{self.foxes:.1f}")
        self.rabbit_value.config(text=f"{self.rabbits:.1f}")
        self.carrot_value.config(text=f"{self.carrots:.1f}")
        
        # Actualizar gráfico
        self.draw_graph()
        
        # Actualizar análisis
        self.update_analysis()
        
        # Actualizar alertas
        self.update_alerts()
    
    def update_analysis(self):
        analysis = ""
        
        if len(self.history['day']) > 1:
            # Tendencias
            fox_trend = "↗ Aumentando" if self.history['foxes'][-1] > self.history['foxes'][-2] else "↘ Disminuyendo"
            rabbit_trend = "↗ Aumentando" if self.history['rabbits'][-1] > self.history['rabbits'][-2] else "↘ Disminuyendo"
            carrot_trend = "↗ Aumentando" if self.history['carrots'][-1] > self.history['carrots'][-2] else "↘ Disminuyendo"
            
            analysis += f"📈 Tendencias: Zorros {fox_trend} | Conejos {rabbit_trend} | Zanahorias {carrot_trend}\n\n"
        
        # Balance del ecosistema
        if self.foxes < 2:
            analysis += "⚠️ Población de zorros muy baja - riesgo de extinción\n"
        if self.rabbits < 5:
            analysis += "⚠️ Población de conejos muy baja - los zorros podrían morir de hambre\n"
        if self.carrots < 50:
            analysis += "⚠️ Zanahorias insuficientes - los conejos podrían morir de hambre\n"
        
        if self.foxes > 100:
            analysis += "⚠️ Demasiados zorros - podrían agotar los conejos\n"
        if self.rabbits > 200:
            analysis += "⚠️ Demasiados conejos - podrían agotar las zanahorias\n"
        
        if not analysis:
            analysis = "✅ El ecosistema está en equilibrio. Todas las poblaciones son saludables."
        
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(1.0, analysis)
    
    def update_alerts(self):
        alerts = []
        
        if self.foxes <= 0:
            alerts.append("❌ ¡LOS ZORROS SE HAN EXTINGUIDO!")
        if self.rabbits <= 0:
            alerts.append("❌ ¡LOS CONEJOS SE HAN EXTINGUIDO!")
        if self.carrots <= 0:
            alerts.append("❌ ¡NO QUEDAN ZANAHORIAS!")
        
        if len(self.history['day']) > 10:
            recent_foxes = self.history['foxes'][-5:]
            if all(fox == 0 for fox in recent_foxes):
                alerts.append("⚠️ Los zorros llevan varios días extintos")
            
            recent_rabbits = self.history['rabbits'][-5:]
            if all(rabbit == 0 for rabbit in recent_rabbits):
                alerts.append("⚠️ Los conejos llevan varios días extintos")
        
        if alerts:
            self.alert_frame.pack(fill=tk.X, pady=5)
            self.alert_label.config(text=" | ".join(alerts))
        else:
            self.alert_frame.pack_forget()
    
    def toggle_config(self):
        if self.config_frame.winfo_ismapped():
            self.config_frame.pack_forget()
            self.config_button.config(text="⚙ Configurar", bg="#3b82f6")
        else:
            self.config_frame.pack(fill=tk.X, pady=5)
            self.config_button.config(text="⬆ Ocultar", bg="#1d4ed8")
    
    def reset_button_click(self):
        if messagebox.askyesno("Reiniciar", "¿Estás seguro de que quieres reiniciar la simulación?\nSe perderán todos los datos actuales."):
            self.reset_simulation()
            self.update_display()
            if self.is_running:
                self.toggle_simulation()

def main():
    root = tk.Tk()
    app = EcosystemSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()