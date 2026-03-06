import tkinter as tk
from tkinter import messagebox
import json
import zipfile
import os
import re

# ============================================================
#  ÉTAPE 1 — Convertir les codes couleurs en fichier Procreate
# ============================================================

def hex_to_rgb_normalized(hex_color):
    """Convertit un code hex (#RRGGBB) en valeurs RGB entre 0 et 1."""
    hex_color = hex_color.lstrip("#")
    return [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]

def create_swatches_file(hex_codes, palette_name, output_dir):
    """Crée le fichier .swatches compressé compatible Procreate."""
    color_profile = "KzqhZFd5qeY0dE+vmwHpECsMm4j9bezteTTfhrlJr34="
    swatches = []

    for hex_color in hex_codes:
        components = hex_to_rgb_normalized(hex_color)
        swatches.append({
            "alpha": 1,
            "origin": 2,
            "colorSpace": 0,
            "colorModel": 0,
            "brightness": max(components),
            "components": components,
            "version": "5.0",
            "colorProfile": color_profile,
            "saturation": max(components) - min(components),
            "hue": 0
        })

    data = {
        "name": palette_name,
        "swatches": swatches,
        "colorProfiles": [{
            "colorSpace": 0,
            "hash": color_profile,
            "iccData": "",
            "iccName": "sRGB IEC61966-2.1"
        }]
    }

    os.makedirs(output_dir, exist_ok=True)
    final_path = os.path.join(output_dir, f"{palette_name}.swatches")
    json_content = json.dumps(data, indent=2)

    # On crée un zip avec le JSON dedans (c'est le format .swatches)
    with zipfile.ZipFile(final_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("Swatches.json", json_content)

    return final_path


# =====================================================================
#  ÉTAPE 2 — La fenêtre, les boutons et l'aperçu des couleurs (tkinter)
# =====================================================================

# --- Couleurs de l'interface ---
BG_DARK      = "#1a1a2e"   # fond principal, bleu nuit
BG_CARD      = "#16213e"   # fond des zones de saisie
ACCENT       = "#e94560"   # rose-rouge pour les boutons et accents
TEXT_LIGHT   = "#eaeaea"   # texte principal
TEXT_MUTED   = "#8892a4"   # texte secondaire
BORDER       = "#0f3460"   # bordures subtiles
SUCCESS      = "#4ecca3"   # vert menthe pour les confirmations

HEX_REGEX = re.compile(r"#?[0-9A-Fa-f]{6}")  # détecte les codes hex valides


class PaletteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✦ Palette Procreate Generator")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        # Centrer la fenêtre sur l'écran
        self.root.geometry("520x680")
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 520) // 2
        y = (self.root.winfo_screenheight() - 680) // 2
        self.root.geometry(f"520x680+{x}+{y}")

        self._build_ui()

    def _build_ui(self):
        """Construit tous les éléments visuels de la fenêtre."""

        # --- Titre ---
        header = tk.Frame(self.root, bg=BG_DARK, pady=20)
        header.pack(fill="x")

        tk.Label(
            header,
            text="✦ Palette Generator",
            font=("Georgia", 22, "bold"),
            fg=ACCENT,
            bg=BG_DARK
        ).pack()

        tk.Label(
            header,
            text="pour Procreate",
            font=("Georgia", 11, "italic"),
            fg=TEXT_MUTED,
            bg=BG_DARK
        ).pack()

        # --- Séparateur ---
        tk.Frame(self.root, height=1, bg=BORDER).pack(fill="x", padx=30)

        # --- Nom de la palette ---
        section_name = tk.Frame(self.root, bg=BG_DARK, padx=30, pady=15)
        section_name.pack(fill="x")

        tk.Label(
            section_name,
            text="Nom de la palette",
            font=("Helvetica", 10, "bold"),
            fg=TEXT_MUTED,
            bg=BG_DARK
        ).pack(anchor="w")

        self.name_var = tk.StringVar(value="Ma palette")
        name_entry = tk.Entry(
            section_name,
            textvariable=self.name_var,
            font=("Helvetica", 13),
            bg=BG_CARD,
            fg=TEXT_LIGHT,
            insertbackground=ACCENT,       # curseur de saisie coloré
            relief="flat",
            bd=8
        )
        name_entry.pack(fill="x", ipady=6)

        # --- Codes hex ---
        section_hex = tk.Frame(self.root, bg=BG_DARK, padx=30)
        section_hex.pack(fill="x")

        tk.Label(
            section_hex,
            text="Codes couleurs (un par ligne)",
            font=("Helvetica", 10, "bold"),
            fg=TEXT_MUTED,
            bg=BG_DARK
        ).pack(anchor="w")

        tk.Label(
            section_hex,
            text="ex : #df265d  ou  df265d",
            font=("Helvetica", 9, "italic"),
            fg=BORDER,
            bg=BG_DARK
        ).pack(anchor="w")

        # Zone de texte pour coller les hex
        self.hex_text = tk.Text(
            section_hex,
            height=8,
            font=("Courier", 12),
            bg=BG_CARD,
            fg=TEXT_LIGHT,
            insertbackground=ACCENT,
            relief="flat",
            bd=8,
            wrap="none"
        )
        self.hex_text.pack(fill="x", pady=(5, 0))

        # Pré-remplissage avec un exemple
        self.hex_text.insert("1.0", "#df265d\n#ea6e93\n#ff9cd2\n#fcb4cc\n#fce3eb")

        # Mise à jour de l'aperçu à chaque frappe
        self.hex_text.bind("<KeyRelease>", lambda e: self._update_preview())

        # --- Aperçu des couleurs ---
        section_preview = tk.Frame(self.root, bg=BG_DARK, padx=30, pady=15)
        section_preview.pack(fill="x")

        tk.Label(
            section_preview,
            text="Aperçu",
            font=("Helvetica", 10, "bold"),
            fg=TEXT_MUTED,
            bg=BG_DARK
        ).pack(anchor="w")

        # Canvas = une zone de dessin tkinter où on affichera les carrés colorés
        self.preview_canvas = tk.Canvas(
            section_preview,
            height=50,
            bg=BG_CARD,
            highlightthickness=0
        )
        self.preview_canvas.pack(fill="x", pady=(5, 0))

        # --- Message de statut ---
        self.status_var = tk.StringVar(value="")
        self.status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Helvetica", 10),
            fg=SUCCESS,
            bg=BG_DARK
        )
        self.status_label.pack(pady=(5, 0))

        # --- Bouton Générer ---
        btn_frame = tk.Frame(self.root, bg=BG_DARK, pady=15)
        btn_frame.pack()

        generate_btn = tk.Button(
            btn_frame,
            text="  ✦  Générer la palette  ✦  ",
            font=("Helvetica", 13, "bold"),
            bg=ACCENT,
            fg="white",
            activebackground="#c73652",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2",
            command=self._generate
        )
        generate_btn.pack()

        # --- Info bas de page ---
        tk.Label(
            self.root,
            text="Les fichiers sont enregistrés dans  Palettes_finales/",
            font=("Helvetica", 9),
            fg=TEXT_MUTED,
            bg=BG_DARK
        ).pack(pady=(5, 20))

        # Premier aperçu au démarrage
        self._update_preview()

    def _get_hex_codes(self):
        """Lit la zone de texte et retourne la liste des codes hex valides."""
        raw = self.hex_text.get("1.0", "end")
        # On cherche tous les codes hex dans le texte (avec ou sans #)
        found = HEX_REGEX.findall(raw)
        # On s'assure que chaque code commence par #
        return [f"#{c.lstrip('#').upper()}" for c in found]

    def _update_preview(self):
        """Redessine les carrés colorés dans le canvas d'aperçu."""
        codes = self._get_hex_codes()
        self.preview_canvas.delete("all")  # efface l'ancien aperçu

        if not codes:
            self.preview_canvas.create_text(
                10, 25,
                text="Aucune couleur détectée...",
                fill=TEXT_MUTED,
                anchor="w",
                font=("Helvetica", 10, "italic")
            )
            return

        # Taille de chaque carré coloré
        square_size = 44
        padding = 5
        x = padding

        for hex_color in codes:
            try:
                # Dessine un rectangle coloré
                self.preview_canvas.create_rectangle(
                    x, padding,
                    x + square_size, padding + square_size,
                    fill=hex_color,
                    outline=BG_DARK,
                    width=2
                )
                x += square_size + padding
            except Exception:
                # Si le code est invalide, on ignore silencieusement
                pass

    def _generate(self):
        """Valide les données et crée le fichier .swatches."""
        palette_name = self.name_var.get().strip()
        hex_codes = self._get_hex_codes()

        # Vérifications de base
        if not palette_name:
            messagebox.showwarning("Nom manquant", "Merci de donner un nom à ta palette.")
            return

        if not hex_codes:
            messagebox.showwarning("Couleurs manquantes", "Aucun code couleur valide détecté.")
            return

        # Dossier de sortie (à côté du script)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "Palettes_finales")

        try:
            final_path = create_swatches_file(hex_codes, palette_name, output_dir)
            self.status_var.set(f"✓ Palette créée avec {len(hex_codes)} couleur(s) !")
            messagebox.showinfo(
                "Palette créée !",
                f"✦ {palette_name}.swatches\n\n"
                f"{len(hex_codes)} couleur(s) enregistrée(s)\n\n"
                f"Dossier : {output_dir}"
            )
        except Exception as e:
            messagebox.showerror("Erreur", f"Quelque chose s'est mal passé :\n{e}")


# ============================================================
#  ÉTAPE 3 — LANCEMENT DE L'APPLICATION
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = PaletteApp(root)
    root.mainloop()
