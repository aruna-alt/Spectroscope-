import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

elements = {
    'Fe³⁺': [480, 530],
    'Fe²⁺': [510, 560],
    'Mn²⁺': [520, 580],
    'Cu²⁺': [600, 700],
    'Ni²⁺': [395, 430],
    'Cr³⁺': [570, 620],
    'Co²⁺': [490, 510],
    'Pb²⁺': [510],
    'MnO₄⁻': [525],
    'Cr₂O₇²⁻': [450, 500],
    'Ti³⁺': [500, 600],
    'CuCl₄²⁻': [600, 700],
    'AsO₄³⁻': [500, 600],
    'NO₂⁻': [450, 500],
    'I⁻': [550, 590],
    'SO₄²⁻': [500, 600]
}

def check(elements, peaks, thresh):
    """Check if detected peaks match element reference peaks within a threshold."""
    for element, ref_peaks in elements.items():
        if isinstance(ref_peaks, list):
            match = all(
                any(abs(peak - ref) <= thresh for ref in ref_peaks) for peak in peaks
            )
        else:
            match = any(abs(peak - ref_peaks) <= thresh for peak in peaks)
        
        if match:
            print(f"{element}: Match found")
        else:
            print(f"{element}: No match")

def graph(simg):
    """Process the spectrum image and visualize detected peaks."""
    image = cv2.imread(simg, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"Error: Unable to load the image '{simg}'. Check the file path or file integrity.")
        return

    pixel_positions = np.arange(0, image.shape[1])
    calibration_factor = 2.9  # Calibration factor for converting pixels to wavelength
    wavelengths = pixel_positions * calibration_factor

    # Extract the spectrum
    spectrum = np.sum(image, axis=0)  # Sum along columns

    # Detect peaks
    peaks, _ = find_peaks(spectrum, height=10, threshold=5, distance=5)
    detected_wavelengths = wavelengths[peaks]

    print("Detected Wavelengths:", detected_wavelengths)

    # Plot the spectrum
    plt.style.use('Solarize_Light2')
    plt.figure(figsize=(10, 5))
    plt.plot(wavelengths, spectrum, color='b', linewidth=2)
    plt.scatter(detected_wavelengths, spectrum[peaks], color='red', label='Detected Peaks')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')
    plt.title('Wavelength Spectrum')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Check detected wavelengths against element reference ranges
    check(elements, detected_wavelengths, 10)

    # Plot zoomed-in views for each element
    fig, ax = plt.subplots(4, 4, figsize=(15, 15))
    ax = ax.flatten()
    for i, (element, ref_peaks) in enumerate(elements.items()):
        mini, maxi = min(ref_peaks) - 50, max(ref_peaks) + 50
        ax[i].plot(wavelengths, spectrum, color='b', linewidth=2)
        ax[i].set_xlim([mini, maxi])
        for ref in ref_peaks:
            ax[i].axvline(x=ref, color='red', linestyle='dashed')
        ax[i].set_title(element)
    
    plt.tight_layout()
    plt.show()

# Example usage
graph('Sample.jpg')
