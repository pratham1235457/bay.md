import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import lightkurve as lk
import numpy as np
from astropy.timeseries import LombScargle

class LightCurveAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Light Curve Analysis Tool")
        self.root.geometry("1400x900")
        
        # Variables to store data
        self.tpf = None
        self.lc = None
        self.flat_lc = None
        self.folded_lc = None
        self.bin_size = tk.IntVar(value=300)
        
        # Create main layout
        self.create_widgets()
        
    def create_widgets(self):
        # Top frame for file selection and search
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Search section
        ttk.Label(top_frame, text="Search Star:").grid(row=0, column=0, padx=5)
        self.star_name_var = tk.StringVar(value="WASP-18")
        star_entry = ttk.Entry(top_frame, textvariable=self.star_name_var, width=20)
        star_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(top_frame, text="Mission:").grid(row=0, column=2, padx=5)
        self.mission_var = tk.StringVar(value="TESS")
        mission_combo = ttk.Combobox(top_frame, textvariable=self.mission_var, 
                                     values=["TESS", "Kepler", "K2"], width=10, state="readonly")
        mission_combo.grid(row=0, column=3, padx=5)
        
        ttk.Button(top_frame, text="Search & Download", command=self.search_star).grid(row=0, column=4, padx=5)
        
        # Separator
        ttk.Separator(top_frame, orient='vertical').grid(row=0, column=5, padx=10, sticky=(tk.N, tk.S))
        
        # Load FITS file section
        ttk.Button(top_frame, text="Load FITS File", command=self.load_fits).grid(row=0, column=6, padx=5)
        self.file_label = ttk.Label(top_frame, text="No file loaded")
        self.file_label.grid(row=0, column=7, padx=5)
        
        # Create notebook for different plots
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Configure row and column weights for resizing
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        # Create tabs
        self.create_pixel_tab()
        self.create_lc_tab()
        self.create_flat_lc_tab()
        self.create_binned_lc_tab()
        self.create_periodogram_tab()
        self.create_folded_lc_tab()
        
    def create_pixel_tab(self):
        pixel_frame = ttk.Frame(self.notebook)
        self.notebook.add(pixel_frame, text="Pixel File")
        
        self.pixel_fig = Figure(figsize=(10, 6))
        self.pixel_canvas = FigureCanvasTkAgg(self.pixel_fig, pixel_frame)
        self.pixel_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(self.pixel_canvas, pixel_frame)
        toolbar.update()
        
    def create_lc_tab(self):
        lc_frame = ttk.Frame(self.notebook)
        self.notebook.add(lc_frame, text="Light Curve")
        
        self.lc_fig = Figure(figsize=(10, 6))
        self.lc_canvas = FigureCanvasTkAgg(self.lc_fig, lc_frame)
        self.lc_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(self.lc_canvas, lc_frame)
        toolbar.update()
        
    def create_flat_lc_tab(self):
        flat_frame = ttk.Frame(self.notebook)
        self.notebook.add(flat_frame, text="Flattened LC")
        
        self.flat_fig = Figure(figsize=(10, 6))
        self.flat_canvas = FigureCanvasTkAgg(self.flat_fig, flat_frame)
        self.flat_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(self.flat_canvas, flat_frame)
        toolbar.update()
        
    def create_binned_lc_tab(self):
        binned_frame = ttk.Frame(self.notebook)
        self.notebook.add(binned_frame, text="Binned LC")
        
        # Control frame for slider
        control_frame = ttk.Frame(binned_frame)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        ttk.Label(control_frame, text="Bin Size:").pack(side=tk.LEFT, padx=5)
        self.bin_slider = ttk.Scale(control_frame, from_=10, to=500, 
                                    variable=self.bin_size, orient=tk.HORIZONTAL,
                                    command=self.update_binned_plot)
        self.bin_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.bin_value_label = ttk.Label(control_frame, text=f"Value: {self.bin_size.get()}")
        self.bin_value_label.pack(side=tk.LEFT, padx=5)
        
        self.binned_fig = Figure(figsize=(10, 6))
        self.binned_canvas = FigureCanvasTkAgg(self.binned_fig, binned_frame)
        self.binned_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(self.binned_canvas, binned_frame)
        toolbar.update()
        
    def create_periodogram_tab(self):
        period_frame = ttk.Frame(self.notebook)
        self.notebook.add(period_frame, text="Periodogram")
        
        self.period_fig = Figure(figsize=(10, 6))
        self.period_canvas = FigureCanvasTkAgg(self.period_fig, period_frame)
        self.period_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Label to display best period
        self.period_label = ttk.Label(period_frame, text="Best Period: N/A")
        self.period_label.pack(side=tk.BOTTOM, pady=5)
        
        toolbar = NavigationToolbar2Tk(self.period_canvas, period_frame)
        toolbar.update()
        
    def create_folded_lc_tab(self):
        folded_frame = ttk.Frame(self.notebook)
        self.notebook.add(folded_frame, text="Folded LC")
        
        self.folded_fig = Figure(figsize=(10, 6))
        self.folded_canvas = FigureCanvasTkAgg(self.folded_fig, folded_frame)
        self.folded_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(self.folded_canvas, folded_frame)
        toolbar.update()
        
    def search_star(self):
        """Search for a star and download its target pixel file"""
        star_name = self.star_name_var.get().strip()
        mission = self.mission_var.get()
        
        if not star_name:
            messagebox.showwarning("Input Required", "Please enter a star name")
            return
            
        try:
            # Show loading message
            self.file_label.config(text=f"Searching for {star_name}...")
            self.root.update()
            
            # Search and download the target pixel file
            search_result = lk.search_targetpixelfile(star_name, mission=mission)
            
            if len(search_result) == 0:
                messagebox.showwarning("Not Found", 
                                      f"No data found for {star_name} in {mission} mission")
                self.file_label.config(text="No file loaded")
                return
            
            # Download with hardest quality bitmask
            self.tpf = search_result.download(quality_bitmask="hardest")
            
            if self.tpf is None:
                messagebox.showerror("Download Error", 
                                    f"Failed to download data for {star_name}")
                self.file_label.config(text="No file loaded")
                return
            
            self.file_label.config(text=f"Loaded: {star_name} ({mission})")
            
            # Extract light curve
            self.lc = self.tpf.to_lightcurve(aperture_mask='all')
            
            # Flatten light curve
            self.flat_lc = self.lc.flatten(window_length=401)
            
            # Update all plots
            self.plot_pixel_file()
            self.plot_light_curve()
            self.plot_flat_light_curve()
            self.plot_binned_light_curve()
            self.plot_periodogram()
            self.plot_folded_light_curve()
            
            messagebox.showinfo("Success", 
                              f"Successfully loaded and analyzed {star_name}!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error searching for star:\n{str(e)}")
            self.file_label.config(text="No file loaded")
        
    def load_fits(self):
        filename = filedialog.askopenfilename(
            title="Select FITS file",
            filetypes=[("FITS files", "*.fits"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # Load the target pixel file
                self.tpf = lk.read(filename)
                self.file_label.config(text=f"Loaded: {filename.split('/')[-1]}")
                
                # Extract light curve
                self.lc = self.tpf.to_lightcurve(aperture_mask='all')
                
                # Flatten light curve
                self.flat_lc = self.lc.flatten(window_length=401)
                
                # Update all plots
                self.plot_pixel_file()
                self.plot_light_curve()
                self.plot_flat_light_curve()
                self.plot_binned_light_curve()
                self.plot_periodogram()
                self.plot_folded_light_curve()
                
                messagebox.showinfo("Success", "FITS file loaded and analyzed successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error loading FITS file:\n{str(e)}")
                
    def plot_pixel_file(self):
        if self.tpf is None:
            return
            
        self.pixel_fig.clear()
        ax = self.pixel_fig.add_subplot(121)
        
        # Plot the pixel file
        self.tpf.plot(ax=ax, aperture_mask=self.tpf.create_threshold_mask(threshold=5))
        
        ax.set_title("Target Pixel File")
        self.pixel_canvas.draw()
        
    def plot_light_curve(self):
        if self.lc is None:
            return
            
        self.lc_fig.clear()
        ax = self.lc_fig.add_subplot(111)
        
        self.lc.plot(ax=ax)
        ax.set_title("Raw Light Curve")
        ax.set_xlabel("Time (BTJD)")
        ax.set_ylabel("Flux (e-/s)")
        
        self.lc_canvas.draw()
        
    def plot_flat_light_curve(self):
        if self.flat_lc is None:
            return
            
        self.flat_fig.clear()
        ax = self.flat_fig.add_subplot(111)
        
        self.flat_lc.plot(ax=ax)
        ax.set_title("Flattened Light Curve")
        ax.set_xlabel("Time (BTJD)")
        ax.set_ylabel("Normalized Flux")
        
        self.flat_canvas.draw()
        
    def update_binned_plot(self, value=None):
        if self.flat_lc is None:
            return
            
        bin_size = int(float(value)) if value else self.bin_size.get()
        self.bin_value_label.config(text=f"Value: {bin_size}")
        self.plot_binned_light_curve()
        
    def plot_binned_light_curve(self):
        if not hasattr(self, 'folded_lc') or self.folded_lc is None:
            return
            
        self.binned_fig.clear()
        ax = self.binned_fig.add_subplot(111)
        
        bins = self.bin_size.get()
        binned_lc = self.folded_lc.bin(bins=bins)
        
        binned_lc.scatter(ax=ax, label=f'Binned (bins={bins})', s=10)
        ax.set_title(f"Binned Folded Light Curve (Bins: {bins})")
        ax.set_xlabel("Phase")
        ax.set_ylabel("Normalized Flux")
        ax.legend()
        
        self.binned_canvas.draw()
        
    def plot_periodogram(self):
        if self.flat_lc is None:
            return
            
        self.period_fig.clear()
        ax = self.period_fig.add_subplot(111)
        
        try:
            # Create periodogram
            pg = self.flat_lc.to_periodogram()
            
            # Plot periodogram
            pg.plot(ax=ax)
            ax.set_title("Periodogram")
            ax.set_xlabel("Period (days)")
            ax.set_ylabel("Power")
            
            # Find and store best period
            self.best_period = pg.period_at_max_power.value
            self.period_label.config(text=f"Best Period: {self.best_period:.6f} days")
            
            # Mark the maximum power
            ax.axvline(self.best_period, color='r', linestyle='--', 
                      label=f'Best Period: {self.best_period:.6f} days')
            ax.legend()
            
            self.period_canvas.draw()
            
        except Exception as e:
            print(f"Error creating periodogram: {e}")
            
    def plot_folded_light_curve(self):
        if self.flat_lc is None or not hasattr(self, 'best_period'):
            return
            
        self.folded_fig.clear()
        ax = self.folded_fig.add_subplot(111)
        
        try:
            # Fold the light curve with best period
            self.folded_lc = self.flat_lc.fold(period=self.best_period)
            
            self.folded_lc.scatter(ax=ax)
            ax.set_title(f"Folded Light Curve (Period: {self.best_period:.6f} days)")
            ax.set_xlabel("Phase")
            ax.set_ylabel("Normalized Flux")
            
            self.folded_canvas.draw()
            
        except Exception as e:
            print(f"Error creating folded light curve: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LightCurveAnalysisApp(root)
    root.mainloop()
