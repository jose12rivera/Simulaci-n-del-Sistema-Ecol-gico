import tkinter as tk
from tkinter import ttk, messagebox
import math

class EcosystemSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("🦊 Simulador de Ecosistema - Parque Nacional")
        
        # Configurar para pantalla completa
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#f0f9ff")
        
        # Botón para salir de pantalla completa (opcional)
        self.root.bind("<Escape>", lambda e: self.root.attributes('-fullscreen', False))
        self.root.bind("<F11>", lambda e: self.root.attributes('-fullscreen', 
                          not self.root.attributes('-fullscreen')))
        
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
        # Crear frame principal con scrollbar
        main_container = tk.Frame(self.root, bg="#f0f9ff")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Crear canvas y scrollbar
        self.canvas = tk.Canvas(main_container, bg="#f0f9ff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=self.canvas.yview)
        
        # Frame principal que contendrá todo el contenido
        self.main_frame = tk.Frame(self.canvas, bg="#f0f9ff")
        
        # Configurar el canvas para el scroll
        self.main_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Crear ventana en el canvas
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar canvas y scrollbar
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar el scroll con la rueda del mouse
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.main_frame.bind("<MouseWheel>", self._on_mousewheel)
        
        # Header
        self.create_header(self.main_frame)
        
        # Frame de alertas
        self.alert_frame = tk.Frame(self.main_frame, bg="#fee2e2", relief=tk.RIDGE, bd=2)
        self.alert_label = tk.Label(self.alert_frame, text="", bg="#fee2e2", 
                                    fg="#991b1b", font=("Arial", 12, "bold"), 
                                    justify=tk.LEFT, wraplength=1800)
        self.alert_label.pack(padx=15, pady=10)
        
        # Frame de estadísticas
        stats_frame = tk.Frame(self.main_frame, bg="#f0f9ff")
        stats_frame.pack(fill=tk.X, pady=15)
        
        self.create_stat_cards(stats_frame)
        
        # Frame de configuración
        self.config_frame = tk.Frame(self.main_frame, bg="white", relief=tk.RIDGE, bd=2)
        self.create_config_panel()
        
        # Frame del gráfico con selector
        graph_container = tk.Frame(self.main_frame, bg="white", relief=tk.RIDGE, bd=2)
        graph_container.pack(fill=tk.BOTH, expand=True, pady=15)
        
        # Selector de tipo de gráfico
        selector_frame = tk.Frame(graph_container, bg="white")
        selector_frame.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(selector_frame, text="📊 Tipo de Gráfico:", 
                bg="white", fg="#1f2937", font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=(0, 20))
        
        btn_line = tk.Button(selector_frame, text="📈 Líneas", 
                            command=lambda: self.change_graph("line"),
                            bg="#3b82f6", fg="white", font=("Arial", 12, "bold"),
                            padx=20, pady=8, cursor="hand2", relief=tk.FLAT)
        btn_line.pack(side=tk.LEFT, padx=8)
        
        btn_bar = tk.Button(selector_frame, text="📊 Barras", 
                           command=lambda: self.change_graph("bar"),
                           bg="#8b5cf6", fg="white", font=("Arial", 12, "bold"),
                           padx=20, pady=8, cursor="hand2", relief=tk.FLAT)
        btn_bar.pack(side=tk.LEFT, padx=8)
        
        btn_pie = tk.Button(selector_frame, text="🥧 Pastel", 
                           command=lambda: self.change_graph("pie"),
                           bg="#ec4899", fg="white", font=("Arial", 12, "bold"),
                           padx=20, pady=8, cursor="hand2", relief=tk.FLAT)
        btn_pie.pack(side=tk.LEFT, padx=8)
        
        # Botón para pantalla completa
        btn_fullscreen = tk.Button(selector_frame, text="⛶ Pantalla Completa", 
                                  command=self.toggle_fullscreen,
                                  bg="#10b981", fg="white", font=("Arial", 10, "bold"),
                                  padx=15, pady=6, cursor="hand2", relief=tk.FLAT)
        btn_fullscreen.pack(side=tk.RIGHT, padx=8)
        
        self.graph_buttons = {"line": btn_line, "bar": btn_bar, "pie": btn_pie}
        
        self.create_graph_canvas(graph_container)
        
        # Frame de análisis
        self.analysis_frame = tk.Frame(self.main_frame, bg="white", relief=tk.RIDGE, bd=2)
        self.analysis_frame.pack(fill=tk.X, pady=15)
        
        analysis_title = tk.Label(self.analysis_frame, text="💡 Análisis y Recomendaciones", 
                                 bg="white", fg="#1f2937", font=("Arial", 16, "bold"))
        analysis_title.pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        self.analysis_text = tk.Text(self.analysis_frame, height=8, wrap=tk.WORD, 
                                    font=("Arial", 12), relief=tk.FLAT, bg="#f9fafb")
        self.analysis_text.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Añadir más contenido para hacer scroll necesario
        self.create_additional_content()
        
    def toggle_fullscreen(self):
        """Alternar entre pantalla completa y ventana normal"""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)
        
    def _on_mousewheel(self, event):
        """Manejar el scroll del mouse"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
    def create_additional_content(self):
        """Crear contenido adicional para hacer el scroll más útil"""
        # Información adicional sobre el ecosistema
        info_frame = tk.Frame(self.main_frame, bg="white", relief=tk.RIDGE, bd=2)
        info_frame.pack(fill=tk.X, pady=15)
        
        info_title = tk.Label(info_frame, text="📋 Información del Ecosistema", 
                             bg="white", fg="#1f2937", font=("Arial", 16, "bold"))
        info_title.pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        info_text = """
Este simulador representa un ecosistema simplificado con tres componentes principales:

🦊 ZORROS (Depredadores):
- Se alimentan de conejos
- Tienen una tasa de mortalidad natural
- Su población crece cuando hay suficiente comida

🐰 CONEJOS (Herbívoros):
- Se alimentan de zanahorias
- Son presa de los zorros
- Tienen tasa de reproducción y mortalidad natural

🥕 ZANAHORIAS (Recursos):
- Crecen a una tasa constante
- Son consumidas por los conejos
- Tienen un límite máximo de crecimiento

El equilibrio del ecosistema depende de la interacción entre estas tres poblaciones.
Si alguna población se extingue, todo el sistema puede colapsar.
"""
        
        info_label = tk.Label(info_frame, text=info_text, bg="white", fg="#374151",
                             font=("Arial", 12), justify=tk.LEFT, wraplength=1800)
        info_label.pack(anchor=tk.W, padx=20, pady=(0, 15))
        
        # Consejos de uso
        tips_frame = tk.Frame(self.main_frame, bg="white", relief=tk.RIDGE, bd=2)
        tips_frame.pack(fill=tk.X, pady=15)
        
        tips_title = tk.Label(tips_frame, text="💡 Consejos de Uso", 
                             bg="white", fg="#1f2937", font=("Arial", 16, "bold"))
        tips_title.pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        tips_text = """
• Comienza con los valores predeterminados para ver un ecosistema equilibrado
• Experimenta cambiando las poblaciones iniciales en la configuración
• Observa cómo los gráficos muestran las tendencias a lo largo del tiempo
• Presta atención a las alertas cuando las poblaciones estén en peligro
• Usa los diferentes tipos de gráficos para analizar los datos de distintas formas
• El gráfico de pastel muestra la distribución actual de las poblaciones
• El gráfico de barras muestra los últimos 20 días de evolución
• El gráfico de líneas muestra toda la historia de la simulación
• Presiona F11 o Escape para alternar pantalla completa
"""
        
        tips_label = tk.Label(tips_frame, text=tips_text, bg="white", fg="#374151",
                             font=("Arial", 12), justify=tk.LEFT, wraplength=1800)
        tips_label.pack(anchor=tk.W, padx=20, pady=(0, 15))
        
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg="white", relief=tk.RIDGE, bd=2)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Título y día
        title_frame = tk.Frame(header_frame, bg="white")
        title_frame.pack(side=tk.LEFT, padx=25, pady=20)
        
        title_label = tk.Label(title_frame, text="🦊 Simulador de Ecosistema - Parque Nacional", 
                              bg="white", fg="#1f2937", font=("Arial", 24, "bold"))
        title_label.pack(anchor=tk.W)
        
        self.day_label = tk.Label(title_frame, text="Día: 0", 
                                 bg="white", fg="#2563eb", font=("Arial", 14, "bold"))
        self.day_label.pack(anchor=tk.W)
        
        # Botones
        button_frame = tk.Frame(header_frame, bg="white")
        button_frame.pack(side=tk.RIGHT, padx=25, pady=20)
        
        self.play_button = tk.Button(button_frame, text="▶ Iniciar", 
                                     command=self.toggle_simulation,
                                     bg="#22c55e", fg="white", font=("Arial", 12, "bold"),
                                     padx=25, pady=10, cursor="hand2", relief=tk.FLAT)
        self.play_button.pack(side=tk.LEFT, padx=8)
        
        reset_button = tk.Button(button_frame, text="↻ Reiniciar", 
                                command=self.reset_button_click,
                                bg="#6b7280", fg="white", font=("Arial", 12, "bold"),
                                padx=25, pady=10, cursor="hand2", relief=tk.FLAT)
        reset_button.pack(side=tk.LEFT, padx=8)
        
        self.config_button = tk.Button(button_frame, text="⚙ Configurar", 
                                       command=self.toggle_config,
                                       bg="#3b82f6", fg="white", font=("Arial", 12, "bold"),
                                       padx=25, pady=10, cursor="hand2", relief=tk.FLAT)
        self.config_button.pack(side=tk.LEFT, padx=8)
        
    def create_stat_cards(self, parent):
        # Tarjeta Zorros
        fox_frame = tk.Frame(parent, bg="#f97316", relief=tk.RIDGE, bd=0)
        fox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)
        
        tk.Label(fox_frame, text="🦊 Zorros", bg="#f97316", fg="white", 
                font=("Arial", 16, "bold")).pack(anchor=tk.W, padx=25, pady=(20, 8))
        
        self.fox_value = tk.Label(fox_frame, text="10.0", bg="#f97316", fg="white", 
                                 font=("Arial", 36, "bold"))
        self.fox_value.pack(anchor=tk.W, padx=25)
        
        self.fox_initial = tk.Label(fox_frame, text=f"Inicial: {self.params['foxes_init']}", 
                                   bg="#f97316", fg="white", font=("Arial", 11))
        self.fox_initial.pack(anchor=tk.W, padx=25, pady=(0, 20))
        
        # Tarjeta Conejos
        rabbit_frame = tk.Frame(parent, bg="#6b7280", relief=tk.RIDGE, bd=0)
        rabbit_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)
        
        tk.Label(rabbit_frame, text="🐰 Conejos", bg="#6b7280", fg="white", 
                font=("Arial", 16, "bold")).pack(anchor=tk.W, padx=25, pady=(20, 8))
        
        self.rabbit_value = tk.Label(rabbit_frame, text="50.0", bg="#6b7280", fg="white", 
                                     font=("Arial", 36, "bold"))
        self.rabbit_value.pack(anchor=tk.W, padx=25)
        
        self.rabbit_initial = tk.Label(rabbit_frame, text=f"Inicial: {self.params['rabbits_init']}", 
                                      bg="#6b7280", fg="white", font=("Arial", 11))
        self.rabbit_initial.pack(anchor=tk.W, padx=25, pady=(0, 20))
        
        # Tarjeta Zanahorias
        carrot_frame = tk.Frame(parent, bg="#fb923c", relief=tk.RIDGE, bd=0)
        carrot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)
        
        tk.Label(carrot_frame, text="🥕 Zanahorias", bg="#fb923c", fg="white", 
                font=("Arial", 16, "bold")).pack(anchor=tk.W, padx=25, pady=(20, 8))
        
        self.carrot_value = tk.Label(carrot_frame, text="200", bg="#fb923c", fg="white", 
                                     font=("Arial", 36, "bold"))
        self.carrot_value.pack(anchor=tk.W, padx=25)
        
        self.carrot_initial = tk.Label(carrot_frame, text=f"Inicial: {self.params['carrots_init']}", 
                                      bg="#fb923c", fg="white", font=("Arial", 11))
        self.carrot_initial.pack(anchor=tk.W, padx=25, pady=(0, 20))
        
    def create_config_panel(self):
        title = tk.Label(self.config_frame, text="⚙️ Configuración del Ecosistema", 
                        bg="white", fg="#1f2937", font=("Arial", 16, "bold"))
        title.pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        # Grid de configuración
        grid_frame = tk.Frame(self.config_frame, bg="white")
        grid_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
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
            frame.grid(row=0, column=col, padx=12, pady=8, sticky="ew")
            
            label = tk.Label(frame, text=label_text, bg="white", fg="#374151", 
                           font=("Arial", 11, "bold"))
            label.pack(anchor=tk.W)
            
            entry = tk.Entry(frame, font=("Arial", 12), relief=tk.SOLID, bd=1)
            entry.insert(0, str(self.params[key]))
            entry.pack(fill=tk.X, pady=(5, 0))
            
            self.config_entries[key] = entry
        
        for col in range(6):
            grid_frame.columnconfigure(col, weight=1)
            
    def create_graph_canvas(self, parent):
        # Crear canvas para el gráfico
        self.canvas_frame = tk.Frame(parent, bg="white")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        self.graph_canvas = tk.Canvas(self.canvas_frame, bg="white", highlightthickness=1, 
                                     highlightbackground="#d1d5db")
        self.graph_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Leyenda
        legend_frame = tk.Frame(self.canvas_frame, bg="white")
        legend_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(legend_frame, text="🦊 Zorros", fg="#f97316", bg="white", 
                font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=25)
        tk.Label(legend_frame, text="🐰 Conejos", fg="#6b7280", bg="white", 
                font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=25)
        tk.Label(legend_frame, text="🥕 Zanahorias", fg="#fb923c", bg="white", 
                font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=25)
    
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
    
    # Los métodos draw_graph, draw_line_graph, draw_bar_graph, draw_3d_bar, draw_pie_chart
    # se mantienen igual que en la versión anterior, pero se adaptan automáticamente
    # al tamaño de pantalla completa
    
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
            
        padding = 80  # Más padding para pantalla grande
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
                                         fill="#e5e7eb", width=2, dash=(2, 4))
            value = max_value * (1 - i / 4)
            self.graph_canvas.create_text(padding - 15, y, text=f"{value:.0f}", 
                                         anchor=tk.E, font=("Arial", 11), fill="#6b7280")
        
        # Dibujar ejes principales (más gruesos)
        self.graph_canvas.create_line(padding, height - padding, width - padding, 
                                     height - padding, width=4, fill="#374151")
        self.graph_canvas.create_line(padding, padding, padding, height - padding, 
                                     width=4, fill="#374151")
        
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
        
        # Dibujar las líneas principales (más gruesas)
        if len(points_carrots) >= 4:
            self.graph_canvas.create_line(points_carrots, fill="#fb923c", width=5, 
                                         smooth=True, capstyle=tk.ROUND)
        if len(points_rabbits) >= 4:
            self.graph_canvas.create_line(points_rabbits, fill="#6b7280", width=5, 
                                         smooth=True, capstyle=tk.ROUND)
        if len(points_foxes) >= 4:
            self.graph_canvas.create_line(points_foxes, fill="#f97316", width=5, 
                                         smooth=True, capstyle=tk.ROUND)
        
        # Dibujar puntos destacados (más grandes)
        for i in range(0, len(points_foxes), 4):
            if i < len(points_foxes):
                x, y = points_foxes[i], points_foxes[i+1]
                self.graph_canvas.create_oval(x-6, y-6, x+6, y+6, fill="#f97316", 
                                             outline="white", width=2)
        
        # Etiquetas (más grandes)
        self.graph_canvas.create_text(width // 2, height - 30, text="Días", 
                                     font=("Arial", 14, "bold"), fill="#1f2937")
        self.graph_canvas.create_text(30, height // 2, text="Población", angle=90, 
                                     font=("Arial", 14, "bold"), fill="#1f2937")
    
    def draw_bar_graph(self):
        if len(self.history['day']) < 1:
            return
            
        self.graph_canvas.delete("all")
        
        width = self.graph_canvas.winfo_width()
        height = self.graph_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
            
        padding = 80  # Más padding para pantalla grande
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
                                         fill="#e5e7eb", width=2, dash=(2, 4))
            value = max_value * (1 - i / 4)
            self.graph_canvas.create_text(padding - 15, y, text=f"{value:.0f}", 
                                         anchor=tk.E, font=("Arial", 11), fill="#6b7280")
        
        # Dibujar ejes (más gruesos)
        self.graph_canvas.create_line(padding, height - padding, width - padding, 
                                     height - padding, width=4, fill="#374151")
        self.graph_canvas.create_line(padding, padding, padding, height - padding, 
                                     width=4, fill="#374151")
        
        # Calcular ancho de barras (más anchas)
        bar_group_width = graph_width / days_to_show
        bar_width = bar_group_width / 3.5  # Barras más anchas
        
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
                self.graph_canvas.create_text(x, height - padding + 20, 
                                             text=f"D{days[i]}", 
                                             font=("Arial", 10), fill="#6b7280")
        
        # Etiquetas (más grandes)
        self.graph_canvas.create_text(width // 2, height - 30, text="Días", 
                                     font=("Arial", 14, "bold"), fill="#1f2937")
        self.graph_canvas.create_text(30, height // 2, text="Población", angle=90, 
                                     font=("Arial", 14, "bold"), fill="#1f2937")
    
    def draw_3d_bar(self, x1, y1, x2, y2, color, dark_color):
        # Sombra - usar gris claro en lugar de transparencia
        self.graph_canvas.create_rectangle(x1 + 4, y1 + 4, x2 + 4, y2 + 4, 
                                          fill="#d1d5db", outline="")
        
        # Barra principal con gradiente simulado
        bar_height = y2 - y1
        steps = max(1, int(bar_height / 6))  # Más pasos para mejor gradiente
        
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
        
        # Borde (más grueso)
        self.graph_canvas.create_rectangle(x1, y1, x2, y2, outline="white", width=3)
        
        # Brillo superior - usar gris muy claro
        self.graph_canvas.create_rectangle(x1, y1, x2, y1 + 6, 
                                          fill="#f8fafc", outline="")
    
    def draw_pie_chart(self):
        if self.foxes == 0 and self.rabbits == 0 and self.carrots == 0:
            return
            
        self.graph_canvas.delete("all")
        
        width = self.graph_canvas.winfo_width()
        height = self.graph_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Centro y radio del gráfico (más grande)
        center_x = width // 2
        center_y = height // 2
        radius = min(width, height) // 2.5  # Gráfico más grande
        
        # Calcular totales
        total = self.foxes + self.rabbits + self.carrots
        if total == 0:
            return
        
        # Calcular ángulos
        fox_angle = (self.foxes / total) * 360
        rabbit_angle = (self.rabbits / total) * 360
        carrot_angle = (self.carrots / total) * 360
        
        # Dibujar título (más grande)
        self.graph_canvas.create_text(center_x, 40, 
                                     text="Distribución Actual del Ecosistema", 
                                     font=("Arial", 18, "bold"), fill="#1f2937")
        
        # Ángulo de inicio
        start_angle = 0
        
        # Lista de segmentos
        segments = [
            (fox_angle, "#f97316", "#ea580c", "🦊 Zorros", self.foxes),
            (rabbit_angle, "#6b7280", "#4b5563", "🐰 Conejos", self.rabbits),
            (carrot_angle, "#fb923c", "#ea580c", "🥕 Zanahorias", self.carrots)
        ]
        
        # Dibujar sombra - usar gris claro
        self.graph_canvas.create_oval(center_x - radius + 6, center_y - radius + 6,
                                     center_x + radius + 6, center_y + radius + 6,
                                     fill="#e5e7eb", outline="")
        
        # Dibujar segmentos
        for angle, color, dark_color, label, value in segments:
            if angle > 0:
                # Segmento principal (más grueso)
                self.graph_canvas.create_arc(center_x - radius, center_y - radius,
                                            center_x + radius, center_y + radius,
                                            start=start_angle, extent=angle,
                                            fill=color, outline="white", width=4)
                
                # Efecto 3D (borde oscuro)
                self.graph_canvas.create_arc(center_x - radius + 3, center_y - radius + 3,
                                            center_x + radius - 3, center_y + radius - 3,
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
                
                # Dibujar etiqueta con fondo (más grande)
                text = f"{percentage:.1f}%"
                self.graph_canvas.create_oval(label_x - 35, label_y - 25,
                                            label_x + 35, label_y + 25,
                                            fill="white", outline=color, width=3)
                self.graph_canvas.create_text(label_x, label_y, text=text,
                                            font=("Arial", 12, "bold"), fill=color)
                
                start_angle += angle
        
        # Círculo central para efecto donut
        inner_radius = radius * 0.4
        self.graph_canvas.create_oval(center_x - inner_radius, center_y - inner_radius,
                                     center_x + inner_radius, center_y + inner_radius,
                                     fill="white", outline="#e5e7eb", width=3)
        
        # Texto central (más grande)
        self.graph_canvas.create_text(center_x, center_y - 12, text="Total",
                                     font=("Arial", 14, "bold"), fill="#6b7280")
        self.graph_canvas.create_text(center_x, center_y + 18, text=f"{int(total)}",
                                     font=("Arial", 24, "bold"), fill="#1f2937")
        
        # Leyenda detallada
        legend_y = height - 120
        legend_x_start = 60
        
        for i, (angle, color, dark_color, label, value) in enumerate(segments):
            x = legend_x_start + (i * (width - 120) // 3)
            
            # Cuadro de color (más grande)
            self.graph_canvas.create_rectangle(x, legend_y, x + 35, legend_y + 35,
                                             fill=color, outline="white", width=3)
            
            # Texto (más grande)
            self.graph_canvas.create_text(x + 45, legend_y + 8, text=label,
                                         anchor=tk.W, font=("Arial", 12, "bold"),
                                         fill=color)
            
            percentage = (value / total) * 100
            self.graph_canvas.create_text(x + 45, legend_y + 28,
                                         text=f"{value:.1f} ({percentage:.1f}%)",
                                         anchor=tk.W, font=("Arial", 10),
                                         fill="#6b7280")

    # Los métodos restantes (toggle_simulation, run_simulation, simulate_day, update_display,
    # update_analysis, update_alerts, toggle_config, reset_button_click) se mantienen igual
    
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