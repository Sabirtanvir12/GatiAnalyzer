import tkinter as tk
from tkinter import ttk
import speedtest
import socket
import requests
import time
import threading
from ping3 import ping
from tkinter import PhotoImage

class TacticalNetworkAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("GatiAnalyzer - By SABIR")
        self.root.geometry("800x600")
        self.root.configure(bg='#121a24')
        
        # Configuration
        self.PING_TARGETS = ['8.8.8.8', '1.1.1.1', '208.67.222.222']
        
        # Color scheme
        self.camo_green = '#3a5f56'
        self.military_dark = '#121a24'
        self.tactical_red = '#c44b4f'
        self.sand_brown = '#d4b483'
        self.hud_green = '#7cfc00'
        self.panel_bg = '#1a2432'
        
        # Network attributes
        self.public_ip = "N/A"
        self.isp_info = "N/A"
        self.server_location = "N/A"
        self.local_ip = "N/A"
        self.abort_test = False
        self.test_running = False
        
        # Initialize UI
        self.create_main_frame()
        self.create_detection_panel()
        self.create_speed_panel()
        self.create_control_panel()
        
        # Initial scan
        self.perform_initial_scan()

    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg=self.military_dark)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_detection_panel(self):
        detection_frame = tk.Frame(self.main_frame, bg=self.panel_bg, bd=2, relief=tk.RIDGE)
        detection_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Header with reload button
        header_frame = tk.Frame(detection_frame, bg=self.panel_bg)
        header_frame.pack(fill=tk.X, pady=(5, 5))
        
        tk.Label(header_frame, text="NETWORK INFORMATION - By GatiAnalyzer", 
                 font=('Impact', 14), fg=self.sand_brown, bg=self.panel_bg).pack(side=tk.TOP, padx=10)
        
        try:
            self.reload_icon = PhotoImage(data="""
                iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBI
                WXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4AkEEjIZ0h5Y9QAAAB1pVFh0Q29tbWVudAAAAAAAQ3Jl
                YXRlZCB3aXRoIEdJTVBkLmUHAAAAJUlEQVQ4y2NgGAXDFmzatMmKAQ38f//+vT8qLzCgYcYoGAWj
                gA4AAK7ZBQ0NcpjZAAAAAElFTkSuQmCC
            """)
            reload_btn = tk.Button(header_frame, image=self.reload_icon, command=self.perform_initial_scan,
                                   bg=self.panel_bg, activebackground=self.panel_bg, bd=0)
            reload_btn.pack(side=tk.RIGHT, padx=10)
            reload_btn.image = self.reload_icon
        except:
            reload_btn = tk.Button(header_frame, text="Reload", command=self.perform_initial_scan,
                                   font=('Arial', 10), bg=self.camo_green, fg=self.sand_brown, bd=0)
            reload_btn.pack(side=tk.TOP, padx=10)
        
        # Information grid
        info_grid = tk.Frame(detection_frame, bg=self.panel_bg)
        info_grid.pack(pady=5)
        
        labels = [
            ("Public IP       :", "ip_label"),
            ("ISP Info        :", "isp_label"),
            ("Server Info   :", "server_label"),
            ("Local IP        :", "local_ip_label")
        ]
        
        for text, tag in labels:
            frame = tk.Frame(info_grid, bg=self.panel_bg)
            frame.pack(anchor='w', pady=2)
            tk.Label(frame, text=text, font=('Arial', 10, 'bold'), 
                     fg=self.sand_brown, bg=self.panel_bg, width=16, anchor='w').pack(side=tk.LEFT)
            label = tk.Label(frame, text="[ Scanning... ]", font=('Consolas', 10), 
                             fg=self.hud_green, bg=self.panel_bg, width=40, anchor='w')
            label.pack(side=tk.LEFT)
            setattr(self, tag, label)

    def perform_initial_scan(self):
        def scan_network():
            # Reset labels
            self.root.after(0, lambda: self.ip_label.config(text="[ Scanning... ]"))
            self.root.after(0, lambda: self.isp_label.config(text="[ Scanning... ]"))
            self.root.after(0, lambda: self.server_label.config(text="[ Scanning... ]"))
            self.root.after(0, lambda: self.local_ip_label.config(text="[ Scanning... ]"))
            
            try:
                # Get public IP and ISP info with location
                self.public_ip = requests.get('https://api.ipify.org', timeout=5).text
                ip_info = requests.get(f'http://ip-api.com/json/{self.public_ip}', timeout=5).json()
                self.isp_info = f"{ip_info.get('isp', 'Unknown ISP')} | {ip_info.get('city', 'Unknown')}, {ip_info.get('country', 'Unknown')}"
            except:
                try:
                    self.public_ip = requests.get('https://ident.me', timeout=5).text
                except:
                    self.public_ip = "N/A"
                    self.isp_info = "Unknown ISP | Location unavailable"

            try:
                # Get local IP
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 53))
                self.local_ip = s.getsockname()[0]
                s.close()
            except Exception as e:
                self.local_ip = socket.gethostbyname(socket.gethostname())

            try:
                # Get server location details
                st = speedtest.Speedtest()
                st.get_best_server()
                best = st.results.server
                self.server_location = f"{best['sponsor']} | {best['name']} | {best['country']}"
            except:
                self.server_location = "Unknown Server | Location unavailable"

            self.root.after(0, self.update_detection_labels)
        
        threading.Thread(target=scan_network, daemon=True).start()

    def update_detection_labels(self):
        self.ip_label.config(text=self.public_ip)
        self.isp_label.config(text=self.isp_info)
        self.server_label.config(text=self.server_location)
        self.local_ip_label.config(text=self.local_ip)

    def create_speed_panel(self):
        speed_frame = tk.Frame(self.main_frame, bg=self.panel_bg)
        speed_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(speed_frame, text="BANDWIDTH METRICS", 
                font=('Impact', 14), fg=self.sand_brown, bg=self.panel_bg).pack(pady=(10, 20))
        
        results_frame = tk.Frame(speed_frame, bg=self.panel_bg)
        results_frame.pack()
        
        # Download
        tk.Label(results_frame, text="DOWNLOAD", font=('Arial', 10, 'bold'), 
                fg=self.sand_brown, bg=self.panel_bg).grid(row=0, column=0, padx=10)
        self.download_label = tk.Label(results_frame, text="0.00", font=('Courier', 28, 'bold'), 
                                      fg=self.hud_green, bg=self.panel_bg)
        self.download_label.grid(row=1, column=0, padx=10)
        tk.Label(results_frame, text="Mbps", font=('Arial', 10), 
                fg=self.sand_brown, bg=self.panel_bg).grid(row=2, column=0)
        
        # Upload
        tk.Label(results_frame, text="UPLOAD", font=('Arial', 10, 'bold'), 
                fg=self.sand_brown, bg=self.panel_bg).grid(row=0, column=1, padx=10)
        self.upload_label = tk.Label(results_frame, text="0.00", font=('Courier', 28, 'bold'), 
                                    fg=self.hud_green, bg=self.panel_bg)
        self.upload_label.grid(row=1, column=1, padx=10)
        tk.Label(results_frame, text="Mbps", font=('Arial', 10), 
                fg=self.sand_brown, bg=self.panel_bg).grid(row=2, column=1)
        
        # Ping
        tk.Label(results_frame, text="PING", font=('Arial', 10, 'bold'), 
                fg=self.sand_brown, bg=self.panel_bg).grid(row=0, column=2, padx=10)
        self.ping_label = tk.Label(results_frame, text="--", font=('Courier', 28, 'bold'), 
                                  fg=self.tactical_red, bg=self.panel_bg)
        self.ping_label.grid(row=1, column=2, padx=10)
        tk.Label(results_frame, text="ms", font=('Arial', 10), 
                fg=self.sand_brown, bg=self.panel_bg).grid(row=2, column=2)

    def create_control_panel(self):
        control_frame = tk.Frame(self.main_frame, bg=self.military_dark)
        control_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.test_button = tk.Button(
            control_frame,
            text="START SCAN",
            command=self.toggle_speed_test,
            font=('Impact', 12),
            bg=self.camo_green,
            fg='white',
            activebackground=self.sand_brown,
            padx=20,
            pady=5
        )
        self.test_button.pack(pady=10)
        
        tk.Button(
            control_frame,
            text="PING TEST",
            command=self.perform_ping_test,
            font=('Arial', 10),
            bg=self.camo_green,
            fg='white'
        ).pack(pady=5)
        
        self.status_label = tk.Label(
            control_frame,
            text="SYSTEM STATUS: STANDBY",
            font=('Consolas', 10),
            fg=self.hud_green,
            bg=self.military_dark
        )
        self.status_label.pack(pady=10)

    def toggle_speed_test(self):
        if self.test_running:
            self.abort_test = True
            self.test_button.config(text="TERMINATING...")
        else:
            self.abort_test = False
            self.test_running = True
            self.test_button.config(text="ABORT SCAN", bg=self.tactical_red)
            self.status_label.config(text="Initializing network scan...")
            threading.Thread(target=self.run_speed_test, daemon=True).start()

    def run_speed_test(self):
        try:
            st = speedtest.Speedtest()
            
            self.update_status("Locating optimal server...")
            st.get_best_server()
            
            self.update_status("Testing download speed...")
            download_speed = st.download() / 1_000_000
            self.root.after(0, lambda: self.download_label.config(text=f"{download_speed:.2f}"))
            
            if self.abort_test:
                raise Exception("Test aborted by user")
                
            self.update_status("Testing upload speed...")
            upload_speed = st.upload() / 1_000_000
            self.root.after(0, lambda: self.upload_label.config(text=f"{upload_speed:.2f}"))
            
            if self.abort_test:
                raise Exception("Test aborted by user")
                
            self.update_status("Testing latency(ping)...")
            ping_result = self.perform_ping_test(update_ui=True)
            
            self.update_status(f"Scan complete | Download: {download_speed:.2f} Mbps | Upload: {upload_speed:.2f} Mbps | Ping: {ping_result:.1f} ms")
            
        except Exception as e:
            self.update_status(f"ERROR: {str(e)}")
        finally:
            self.test_running = False
            self.abort_test = False
            self.root.after(0, lambda: self.test_button.config(
                text="START SCAN",
                bg=self.camo_green
            ))

    def perform_ping_test(self, update_ui=False):
        try:
            latencies = []
            for target in self.PING_TARGETS:
                if self.abort_test:
                    return 0
                    
                response = ping(target, unit='ms', timeout=2)
                if response is not None:
                    latencies.append(response)
                if len(latencies) >= 3:
                    break
            
            avg_ping = sum(latencies)/len(latencies) if latencies else 0
            
            if update_ui:
                self.root.after(0, lambda: self.ping_label.config(text=f"{avg_ping:.1f}"))
                return avg_ping
            else:
                self.update_status(f"Ping test complete | Average: {avg_ping:.1f} ms")
                return avg_ping
                
        except Exception as e:
            self.update_status(f"Ping test failed: {str(e)}")
            return 0

    def update_status(self, message):
        self.root.after(0, lambda: self.status_label.config(text=message))

if __name__ == "__main__":
    root = tk.Tk()
    try:
        app = TacticalNetworkAnalyzer(root)
        root.mainloop()
    except Exception as e:
        print(f"Application error: {e}")