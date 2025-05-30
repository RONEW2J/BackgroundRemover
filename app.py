import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import PhotoImage
import threading
import os
from PIL import Image, ImageTk
from rembg import remove, new_session
import tempfile
from io import BytesIO
import numpy as np

class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Remover")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)  # Minimum window size
        self.root.configure(bg='#f0f0f0')
        
        # Add weight to root window grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Variables
        self.original_image = None
        self.processed_image = None
        self.original_path = None
        self.session = None
        
        self.setup_ui()
        self.initialize_model()

    def initialize_model(self):
        """Инициализация модели rembg в отдельном потоке"""

        def init_model():
            models_to_try = ['u2net', 'u2netp', 'silueta', 'isnet-general-use']

            for model_name in models_to_try:
                try:
                    self.root.after(0, lambda m=model_name: self.update_status(f"Загрузка модели {m}..."))
                    self.session = new_session(model_name)
                    self.root.after(0, lambda m=model_name: self.update_status(f"Модель {m} загружена успешно"))
                    return
                except Exception as e:
                    print(f"Ошибка загрузки модели {model_name}: {e}")
                    continue

            self.root.after(0, lambda: self.update_status("Ошибка: Не удалось загрузить ни одну модель"))

        thread = threading.Thread(target=init_model)
        thread.daemon = True
        thread.start()

    def reload_model(self):
        """Принудительная перезагрузка модели"""
        self.session = None
        self.update_status("Перезагрузка модели...")
        self.initialize_model()

    def update_status(self, message):
        """Обновление статуса в UI"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
            print(f"Status: {message}") 

    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(main_frame, text="✨ Background Remover",
                               font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#333')
        title_label.pack(pady=(0, 20))

        # Status label
        self.status_label = tk.Label(main_frame, text="Загрузка модели...",
                                     font=('Arial', 10), bg='#f0f0f0', fg='#666')
        self.status_label.pack(pady=5)

        # Upload button (добавляем задержку для загрузки модели)
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=10)

        self.upload_btn = tk.Button(button_frame, text="📁 Выбрать изображение",
                                    command=self.select_image, font=('Arial', 12),
                                    bg='#667eea', fg='white', relief=tk.FLAT,
                                    padx=20, pady=10)
        self.upload_btn.pack(side=tk.LEFT, padx=5)

        # Manual model load button
        self.reload_model_btn = tk.Button(button_frame, text="🔄 Перезагрузить модель",
                                          command=self.reload_model, font=('Arial', 10),
                                          bg='#ffc107', fg='black', relief=tk.FLAT,
                                          padx=15, pady=8)
        self.reload_model_btn.pack(side=tk.LEFT, padx=5)

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=10)
        self.progress.pack_forget()

        # Images frame
        images_frame = tk.Frame(main_frame, bg='#f0f0f0')
        images_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        # Original image frame
        original_frame = tk.Frame(images_frame, bg='white', relief=tk.RAISED, bd=1)
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(original_frame, text="📷 Исходное изображение",
                 font=('Arial', 12, 'bold'), bg='white').pack(pady=5)

        self.original_label = tk.Label(original_frame, bg='white',
                                       text="Изображение не выбрано", fg='#999')
        self.original_label.pack(fill=tk.BOTH, expand=True, pady=5)

        # Processed image frame
        processed_frame = tk.Frame(images_frame, bg='white', relief=tk.RAISED, bd=1)
        processed_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        tk.Label(processed_frame, text="✨ Результат",
                 font=('Arial', 12, 'bold'), bg='white').pack(pady=5)

        self.processed_label = tk.Label(processed_frame, bg='white',
                                        text="Обработка не выполнена", fg='#999')
        self.processed_label.pack(fill=tk.BOTH, expand=True, pady=5)

        # Control buttons
        buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
        buttons_frame.pack(pady=20)

        self.process_btn = tk.Button(buttons_frame, text="🚀 Удалить фон",
                                     command=self.process_image_thread,
                                     font=('Arial', 12, 'bold'),
                                     bg='#28a745', fg='white', relief=tk.FLAT,
                                     padx=20, pady=10, state=tk.DISABLED)
        self.process_btn.pack(side=tk.LEFT, padx=5)

        self.save_btn = tk.Button(buttons_frame, text="💾 Сохранить",
                                  command=self.save_image, font=('Arial', 12),
                                  bg='#17a2b8', fg='white', relief=tk.FLAT,
                                  padx=20, pady=10, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(buttons_frame, text="🔄 Сброс",
                                   command=self.reset_app, font=('Arial', 12),
                                   bg='#6c757d', fg='white', relief=tk.FLAT,
                                   padx=20, pady=10)
        self.reset_btn.pack(side=tk.LEFT, padx=5)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
        )

        if file_path:
            self.original_path = file_path
            self.load_original_image(file_path)
            self.process_btn.config(state=tk.NORMAL)

    def load_original_image(self, path):
        try:
            # Load and resize image for display
            image = Image.open(path)
            # Resize for display while maintaining aspect ratio
            image.thumbnail((300, 300), Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(image)
            self.original_label.config(image=photo, text="")
            self.original_label.image = photo  

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {str(e)}")

    def process_image_thread(self):
        # Run processing in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=self.process_image)
        thread.daemon = True
        thread.start()

    def process_image(self):
        try:
            # Show progress bar
            self.root.after(0, lambda: self.progress.pack(fill=tk.X, pady=10))
            self.root.after(0, lambda: self.progress.start())
            self.root.after(0, lambda: self.process_btn.config(state=tk.DISABLED))

            # Process the image with multiple fallback methods
            output_image = None

            # Method 1: Using session if available
            if self.session is not None:
                try:
                    with open(self.original_path, 'rb') as input_file:
                        input_data = input_file.read()
                    output_data = remove(input_data, session=self.session)
                    output_image = Image.open(BytesIO(output_data))
                    print("Method 1 (with session) успешен")
                except Exception as e1:
                    print(f"Method 1 failed: {e1}")

            # Method 2: Direct remove without session
            if output_image is None:
                try:
                    input_image = Image.open(self.original_path)
                    output_data = remove(input_image)
                    if isinstance(output_data, bytes):
                        output_image = Image.open(BytesIO(output_data))
                    else:
                        output_image = output_data
                    print("Method 2 (direct remove) успешен")
                except Exception as e2:
                    print(f"Method 2 failed: {e2}")

            # Method 3: Convert to bytes first
            if output_image is None:
                try:
                    input_image = Image.open(self.original_path)
                    img_byte_arr = BytesIO()
                    input_image.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    output_data = remove(img_byte_arr)
                    output_image = Image.open(BytesIO(output_data))
                    print("Method 3 (bytes conversion) успешен")
                except Exception as e3:
                    print(f"Method 3 failed: {e3}")

            # Method 4: Simple approach without any preprocessing
            if output_image is None:
                try:
                    with open(self.original_path, 'rb') as f:
                        input_bytes = f.read()
                    output_bytes = remove(input_bytes)
                    output_image = Image.open(BytesIO(output_bytes))
                    print("Method 4 (simple bytes) успешен")
                except Exception as e4:
                    print(f"Method 4 failed: {e4}")

            if output_image is None:
                raise Exception(
                    "Все методы обработки изображения не сработали. Проверьте установку rembg и интернет-соединение.")

            # Ensure RGBA format
            if output_image.mode != 'RGBA':
                output_image = output_image.convert('RGBA')

            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            output_image.save(temp_file.name, 'PNG')

            # Load processed image for display
            display_image = output_image.copy()
            display_image.thumbnail((300, 300), Image.Resampling.LANCZOS)

            # Update UI in main thread
            self.root.after(0, self.update_processed_image, display_image, temp_file.name)

        except Exception as e:
            error_msg = f"Ошибка обработки: {str(e)}"
            print(error_msg)  # Для отладки
            self.root.after(0, lambda: messagebox.showerror("Ошибка", error_msg))
            self.root.after(0, self.stop_progress)

    def update_processed_image(self, image, temp_path):
        try:
            photo = ImageTk.PhotoImage(image)
            self.processed_label.config(image=photo, text="")
            self.processed_label.image = photo

            self.processed_image = temp_path
            self.save_btn.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка отображения: {str(e)}")
        finally:
            self.stop_progress()

    def stop_progress(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.process_btn.config(state=tk.NORMAL)

    def save_image(self):
        if not self.processed_image:
            return

        save_path = filedialog.asksaveasfilename(
            title="Сохранить изображение",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )

        if save_path:
            try:
                # Copy from temp file to selected location
                import shutil
                shutil.copy2(self.processed_image, save_path)
                messagebox.showinfo("Успех", "Изображение сохранено!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка сохранения: {str(e)}")

    def reset_app(self):
        self.original_label.config(image="", text="Изображение не выбрано")
        self.processed_label.config(image="", text="Обработка не выполнена")
        self.original_path = None

        # Clean up temp files
        if hasattr(self, 'processed_image') and self.processed_image:
            try:
                os.unlink(self.processed_image)
            except:
                pass

        self.processed_image = None
        self.process_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)

    def __del__(self):
        # Clean up temp files on exit
        if hasattr(self, 'processed_image') and self.processed_image:
            try:
                os.unlink(self.processed_image)
            except:
                pass


if __name__ == "__main__":
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()