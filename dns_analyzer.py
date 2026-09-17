import tkinter as tk
from tkinter import ttk, messagebox
import dns.resolver

def analyze_dns():
    domain = entry_domain.get().strip()
    
    # Basic cleanup in case the user pastes a URL instead of a domain
    domain = domain.replace("https://", "").replace("http://", "").split("/")[0]
    
    if not domain:
        messagebox.showerror("Input Error", "Please enter a valid domain name (e.g., google.com)")
        return

    text_output.config(state=tk.NORMAL)
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, f"[*] Querying DNS architecture for: {domain}\n")
    text_output.insert(tk.END, "-" * 55 + "\n")
    
    btn_scan.config(state=tk.DISABLED)
    lbl_status.config(text="Querying authoritative servers...", fg="#e67e22")
    root.update()

    # Core DNS records to footprint
    record_types = ['A', 'AAAA', 'MX', 'TXT']
    
    for qtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, qtype)
            text_output.insert(tk.END, f"[{qtype} Records]\n")
            for rdata in answers:
                text_output.insert(tk.END, f"  -> {rdata.to_text()}\n")
        except dns.resolver.NoAnswer:
            text_output.insert(tk.END, f"[{qtype} Records]\n  -> No records found.\n")
        except dns.resolver.NXDOMAIN:
            text_output.insert(tk.END, f"[!] FATAL: Domain '{domain}' does not exist.\n")
            break # Stop querying if the domain is completely invalid
        except Exception as e:
            text_output.insert(tk.END, f"[{qtype} Records]\n  -> Query failed.\n")
        
        text_output.insert(tk.END, "\n")

    text_output.insert(tk.END, "-" * 55 + "\n[*] DNS Analysis Complete.\n")
    text_output.config(state=tk.DISABLED)
    btn_scan.config(state=tk.NORMAL)
    lbl_status.config(text="Analysis Complete", fg="#27ae60")

# --- Tkinter GUI Layout ---
root = tk.Tk()
root.title("NOC Toolkit - DNS Analyzer")
root.geometry("550x450")
root.resizable(False, False)

frame = ttk.Frame(root, padding="15")
frame.pack(fill=tk.BOTH, expand=True)

lbl_title = tk.Label(frame, text="DNS Record Footprinting", font=("Helvetica", 13, "bold"))
lbl_title.pack(anchor="w", pady=(0, 10))

# Input Frame
input_frame = tk.Frame(frame)
input_frame.pack(fill=tk.X, pady=(0, 10))

lbl_domain = tk.Label(input_frame, text="Target Domain:", font=("Helvetica", 10))
lbl_domain.pack(side=tk.LEFT, padx=(0, 5))

entry_domain = ttk.Entry(input_frame, width=30, font=("Helvetica", 10))
entry_domain.pack(side=tk.LEFT, padx=(0, 10))
entry_domain.insert(0, "github.com")

btn_scan = tk.Button(input_frame, text="Analyze Records", command=analyze_dns, bg="#2980b9", fg="white", font=("Helvetica", 9, "bold"))
btn_scan.pack(side=tk.LEFT)

lbl_status = tk.Label(frame, text="Ready", font=("Helvetica", 9, "italic"), fg="#555")
lbl_status.pack(anchor="w", pady=(0, 5))

# Output Console Display
text_frame = tk.Frame(frame)
text_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_output = tk.Text(text_frame, font=("Consolas", 9), bg="#1e1e1e", fg="#00ff00", yscrollcommand=scrollbar.set)
text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
text_output.config(state=tk.DISABLED)
scrollbar.config(command=text_output.yview)

root.mainloop()