import os
import webbrowser
import urllib.parse

# 1. EVITAR VENTANAS DE LOGS INNECESARIAS
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_LOG_MODE'] = 'PYTHON'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.core.window import Window

class FastFoodApp(App):
    def build(self):
        # --- CONFIGURACIÓN DE TEXTOS ---
        self.nombre_emprendimiento = "TU MEJOR OPCIÓN EN COMIDA RÁPIDA"
        self.datos_pago = "[b]BANCO DE VENEZUELA[/b]\nTelf: 04241969926\nC.I: 19.220.552"
        self.advertencia_pago = "[i][color=#FFFF00]Cancele antes de enviar su pedido.\n¡Gracias por su Compra![/color][/i]"
        
        self.menu = {
            "Perro Caliente Clásico": 3.50,
            "Hamburguesa Especial": 7.00,
            "Refresco 1 Litro": 1.50,
            "Papas Fritas Medianas": 3.00
        }
        self.cantidades = {producto: 0 for producto in self.menu}
        self.spinners = [] 

        self.main_layout = BoxLayout(orientation='vertical', padding=[12, 10, 12, 10], spacing=8)
        
        # --- LÓGICA DE FONDO CORREGIDA ---
        with self.main_layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1) 
            self.rect_bg = Rectangle(pos=self.main_layout.pos, size=Window.size)
            
            # Buscamos 'comidarapida.jpg' (Nombre exacto de tu archivo)
            directorio = os.path.dirname(os.path.abspath(__file__))
            ruta_final = os.path.join(directorio, 'comidarapida.jpg')
            
            if os.path.exists(ruta_final):
                self.rect_bg.source = ruta_final
            else:
                # Si falla la ruta absoluta, intentamos carga directa
                self.rect_bg.source = 'comidarapida.jpg'
        
        self.main_layout.bind(size=self._update_background, pos=self._update_background)

        # --- DISEÑO DE LA INTERFAZ ---
        header = Label(text=f"[color=#00FF00][b]{self.nombre_emprendimiento}[/b][/color]", 
                        markup=True, font_size='20sp', size_hint_y=None, height=70)
        self.main_layout.add_widget(header)

        root_scroll = ScrollView(do_scroll_x=False)
        content_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=12, padding=[5, 10, 5, 20])
        content_box.bind(minimum_height=content_box.setter('height'))

        content_box.add_widget(Label(text="[b]SELECCIONE SU PEDIDO[/b]", markup=True, size_hint_y=None, height=40))

        for producto, precio in self.menu.items():
            fila = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, spacing=10)
            
            lbl_box = BoxLayout(size_hint_x=0.7)
            with lbl_box.canvas.before:
                Color(0, 0, 0, 0.75) 
                self.rect_item = RoundedRectangle(pos=lbl_box.pos, size=lbl_box.size, radius=[15])
            lbl_box.bind(size=self._update_rect_generic, pos=self._update_rect_generic)
            
            txt_prod = Label(text=f"[b]{producto}[/b]\n[color=#00FF00]${precio:.2f}[/color]", markup=True, halign='center')
            lbl_box.add_widget(txt_prod)
            
            spin = Spinner(text='0', values=[str(i) for i in range(51)], size_hint_x=0.3)
            spin.bind(text=lambda s, v, p=producto: self.actualizar_total(p, v))
            self.spinners.append(spin)
            
            fila.add_widget(lbl_box)
            fila.add_widget(spin)
            content_box.add_widget(fila)

        # Área de Pago
        pago_box = BoxLayout(orientation='vertical', size_hint_y=None, height=620, spacing=12, padding=[15, 20])
        with pago_box.canvas.before:
            Color(0, 0, 0, 0.85)
            self.rect_pago = RoundedRectangle(pos=pago_box.pos, size=pago_box.size, radius=[20])
        pago_box.bind(size=self._update_rect_generic, pos=self._update_rect_generic)

        self.label_total = Label(text="[b]TOTAL A PAGAR: $0.00[/b]", markup=True, font_size='24sp', color=(0.2, 1, 0.2, 1))
        pago_box.add_widget(self.label_total)
        pago_box.add_widget(Label(text=self.datos_pago, markup=True, halign='center', font_size='16sp'))

        self.input_nombre = TextInput(hint_text="Nombre del Cliente", multiline=False, size_hint_y=None, height=50)
        self.input_extra = TextInput(hint_text="¿Qué ingredientes lleva?", multiline=False, size_hint_y=None, height=50)
        self.input_ref = TextInput(hint_text="Referencia Bancaria", multiline=False, size_hint_y=None, height=50)
        
        pago_box.add_widget(self.input_nombre)
        pago_box.add_widget(self.input_extra)
        pago_box.add_widget(self.input_ref)

        self.btn_send = Button(text="[b]CONFIRMAR PEDIDO ✅[/b]", markup=True, background_color=(0, 0.6, 0.2, 1), size_hint_y=None, height=65)
        self.btn_send.bind(on_release=self.enviar_pedido)
        pago_box.add_widget(self.btn_send)

        self.btn_reset = Button(text="[b]NUEVA ORDEN 🔄[/b]", markup=True, background_color=(0, 0.4, 0.7, 1), size_hint_y=None, height=55)
        self.btn_reset.bind(on_release=self.limpiar_pantalla)
        pago_box.add_widget(self.btn_reset)

        pago_box.add_widget(Label(text=self.advertencia_pago, markup=True, halign='center', font_size='14sp'))

        content_box.add_widget(pago_box)
        root_scroll.add_widget(content_box)
        self.main_layout.add_widget(root_scroll)

        return self.main_layout

    def _update_background(self, instance, value):
        self.rect_bg.pos = instance.pos
        self.rect_bg.size = instance.size

    def _update_rect_generic(self, instance, value):
        for instr in instance.canvas.before.children:
            if isinstance(instr, (Rectangle, RoundedRectangle)):
                instr.pos = instance.pos
                instr.size = instance.size

    def actualizar_total(self, producto, valor):
        self.cantidades[producto] = int(valor)
        total = sum(self.cantidades[p] * self.menu[p] for p in self.menu)
        self.label_total.text = f"[b]TOTAL A PAGAR: ${total:.2f}[/b]"

    def limpiar_pantalla(self, instance):
        for p in self.menu: self.cantidades[p] = 0
        for s in self.spinners: s.text = '0'
        self.input_nombre.text = ""; self.input_extra.text = ""; self.input_ref.text = ""
        self.label_total.text = "[b]TOTAL A PAGAR: $0.00[/b]"
        self.btn_send.text = "[b]CONFIRMAR PEDIDO ✅[/b]"
        self.btn_send.background_color = (0, 0.6, 0.2, 1)

    def enviar_pedido(self, instance):
        nombre = self.input_nombre.text.strip()
        ref = self.input_ref.text.strip()
        extra = self.input_extra.text.strip() or "Sin especificaciones"
        total = sum(self.cantidades[p] * self.menu[p] for p in self.menu)
        
        if total == 0 or not nombre or not ref:
            instance.text = "¡DATOS INCOMPLETOS!"
            instance.background_color = (1, 0, 0, 1)
            return

        items = "".join([f"• {c}x {p}\n" for p, c in self.cantidades.items() if c > 0])
        msg = f"🍔 *ORDEN:* {self.nombre_emprendimiento}\n👤 *Cliente:* {nombre}\n📝 *Pedido:*\n{items}🥗 *Ingredientes:* {extra}\n💰 *TOTAL:* ${total:.2f}\n🔢 *REF:* {ref}"
        webbrowser.open(f"https://wa.me/584241969926?text={urllib.parse.quote(msg)}")

if __name__ == '__main__':
    FastFoodApp().run()
            
