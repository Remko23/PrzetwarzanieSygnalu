from SignalGenerator import *
import matplotlib.pyplot as plt

class SignalVisualizer:
    @staticmethod
    def _plot_common(time_axis, data, ax_time, ax_hist, n_bins, label, color, is_discrete):
        # 1. Wykres czasowy
        if is_discrete:
            ax_time.scatter(time_axis, data, s=2, color=color)
        else:
            ax_time.plot(time_axis, data, color=color, linewidth=1)
        ax_time.set_ylabel(label)
        ax_time.grid(True, linestyle='--', alpha=0.7)

        data_min = np.min(data)
        data_max = np.max(data)

        if np.isclose(data_min, data_max):
            ax_hist.hist(data, bins=1, color=color, edgecolor='black', alpha=0.7)
            ax_hist.set_title(f"Histogram (wartość stała: {data_min:.2f})")
        else:
            ax_hist.hist(data, bins=n_bins, color=color, edgecolor='black', alpha=0.7)

        ax_hist.set_ylabel("Częstość")

    @staticmethod
    def plot_all(signal_generator, n_samples, n_bins, is_discrete=False, title="Analiza Sygnału"):
        signal_generator.reset()
        samples = np.array([next(signal_generator) for _ in range(n_samples)])
        signal_generator.reset()

        time_axis = np.arange(n_samples) / signal_generator.fs

        if not np.iscomplexobj(samples):
            # --- SYGNAŁ RZECZYWISTY ---
            fig, (ax_time, ax_hist) = plt.subplots(2, 1, figsize=(10, 8))
            fig.suptitle(title)
            SignalVisualizer._plot_common(time_axis, samples.real, ax_time, ax_hist, n_bins, "Amplituda", "blue",
                                          is_discrete)
            ax_time.set_title("Przebieg czasowy")
            ax_hist.set_title("Histogram")
        else:
            # --- SYGNAŁ ZESPOLONY ---
            for plot_type in ['re_im', 'mod_ph']:
                fig, axes = plt.subplots(2, 2, figsize=(12, 10))
                fig.suptitle(f"{title} - {plot_type.upper()}")

                if plot_type == 're_im':
                    # Wykres Re i Im
                    SignalVisualizer._plot_common(time_axis, samples.real, axes[0, 0], axes[0, 1], n_bins, "Real",
                                                  "blue", is_discrete)
                    SignalVisualizer._plot_common(time_axis, samples.imag, axes[1, 0], axes[1, 1], n_bins, "Imag",
                                                  "red", is_discrete)
                    axes[0, 0].set_title("Real Part");
                    axes[1, 0].set_title("Imag Part")
                else:
                    # Wykres Moduł i Faza
                    SignalVisualizer._plot_common(time_axis, np.abs(samples), axes[0, 0], axes[0, 1], n_bins, "Mod",
                                                  "purple", is_discrete)
                    SignalVisualizer._plot_common(time_axis, np.angle(samples), axes[1, 0], axes[1, 1], n_bins, "Phase",
                                                  "orange", is_discrete)
                    axes[0, 0].set_title("Modulus (Abs)");
                    axes[1, 0].set_title("Phase (Angle)")

        plt.tight_layout(rect=(0, 0.03, 1, 0.95))
        plt.show()

class SignalVisualizerReal:
    @staticmethod
    def plot_all(signal_generator, n_samples, n_bins, is_discrete = False, title="Analiza Sygnału"):
        samples = [next(signal_generator) for _ in range(n_samples)]

        fs = getattr(signal_generator, 'fs', 1000.0)
        time_axis = np.arange(n_samples) / fs

        fig, (ax_time, ax_hist) = plt.subplots(2, 1, figsize=(10, 8))
        fig.suptitle(title, fontsize=16)

        # --- WYKRES CZASOWY ---
        if is_discrete:
            ax_time.scatter(time_axis, samples, s=2)
        else:
            ax_time.plot(time_axis, samples, color='blue', linewidth=1)
        ax_time.set_title("Przebieg czasowy sygnału")
        ax_time.set_xlabel("Czas [s]")
        ax_time.set_ylabel("Amplituda")
        ax_time.grid(True, linestyle='--', alpha=0.7)

        # --- HISTOGRAM ---
        # Histogram ma mieć możliwość ustawienia liczby przedziałów
        # na wartości 5, 10, 15 i 20, lub płynnie w zakresie zawierającym te wartości
        ax_hist.hist(samples, bins=n_bins, color='green', edgecolor='black', alpha=0.7)
        ax_hist.set_title("Histogram (Rozkład amplitud)")
        ax_hist.set_xlabel("Wartość amplitudy")
        ax_hist.set_ylabel("Częstość występowania")
        ax_hist.grid(True, axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout(rect=(0, 0.03, 1, 0.95))
        plt.show()
