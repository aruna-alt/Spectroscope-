import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Updated element ranges
elements = {
    'Albite (NaAlSi₃O₈)': [400, 500],
    'Azurite (Cu₃(CO₃)₂(OH)₂)': [600, 700],
    'Beryl (Be₃Al₂Si₆O₁₈)': [400, 500],
    'Biotite (K(Mg,Fe)₃(AlSi₃O₁₀)(OH)₂)': [500, 600],
    'Calcite (CaCO₃)': [400, 450],
    'Chalcopyrite (CuFeS₂)': [500, 700],
    'Chlorite ((Mg,Fe)₅Al(Si₃Al)O₁₀(OH)₈)': [500, 550],
    'Copper (Cu)': [600, 700],
    'Epidote (Ca₂(Al,Fe)₃(SiO₄)₃(OH))': [450, 550],
    'Goethite (α-FeO(OH))': [480],
    'Gypsum (CaSO₄·2H₂O)': [450, 500],
    'Hematite (Fe₂O₃)': [450],
    'Iron (Fe)': [400, 500],
    'Kaolinite (Al₂Si₂O₅(OH)₄)': [450, 500],
    'Limonite (FeO(OH)·nH₂O)': [500],
    'Magnetite (Fe₃O₄)': [400, 700],
    'Malachite (Cu₂CO₃(OH)₂)': [600, 700],
    'Manganese (Mn)': [500, 600],
    'Muscovite (KAl₂(AlSi₃O₁₀)(OH)₂)': [450, 550],
    'Olivine ((Mg,Fe)₂SiO₄)': [400, 500],
    'Orthoclase (KAlSi₃O₈)': [400, 450],
    'Pyrite (FeS₂)': [500, 600],
    'Quartz (SiO₂)': [400, 500],
    'Rutile (TiO₂)': [400, 450],
    'Siderite (FeCO₃)': [400, 500],
    'Vermiculite ((Mg,Fe,Al)₃(Al,Si)₄O₁₀(OH)₂·4H₂O)': [450, 500],
    'Zinc (Zn)': [500, 600]
}

def check(elements, peaks, thresh):
    for element, ref_range in elements.items():
        # Check if any peak falls within the range
        if len(ref_range) == 2:  # For ranges
            detected = any(ref_range[0] <= peak <= ref_range[1] for peak in peaks)
        else:  # For single values
            detected = any(abs(peak - ref_range[0]) <= thresh for peak in peaks)
        
        print(element, ':', detected)
        if detected:
            print(f"Detected: {element}")

def graph(simg):
    # Read image as grayscale
    image = cv2.imread(simg, cv2.IMREAD_GRAYSCALE)

    pixel_positions = np.arange(0, image.shape[1])
    calibration_factor = 2.9
    wavelengths = pixel_positions * calibration_factor

    # Extract the spectrum
    spectrum = np.sum(image, axis=0)  # Sum along columns

    # Detect peaks
    peaks = find_peaks(spectrum, height=10, threshold=5, distance=5)
    print("Detected wavelengths:", wavelengths[peaks[0]])

    # Plot spectrum
    plt.style.use('Solarize_Light2')
    fig = plt.figure(figsize=(10, 5))
    plt.plot(wavelengths, spectrum, color='b', linewidth=2)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')
    plt.title('Wavelength Spectrum')
    plt.grid(True)
    plt.show()

    # Check detected peaks against elements
    check(elements, wavelengths[peaks[0]], 10)

    # Plot each element's spectrum range
    fig, ax = plt.subplots(4, 4)
    r, c = 0, 0
    for i in elements:
        mini, maxi = elements[i][0], elements[i][-1] if len(elements[i]) > 1 else elements[i][0] + 50
        ax[r, c].plot(wavelengths, spectrum, color='b', linewidth=2)
        ax[r, c].set_xlim([mini, maxi])
        for j in elements[i]:
            ax[r, c].axvline(x=j, color='red', linestyle='dashed')
        ax[r, c].set_title(i)
        r += 1
        if r > 3:
            r = 0
            c += 1
        if c > 3:
            break

    plt.subplots_adjust(top=0.94, bottom=0.07, left=0.125, right=0.9, hspace=0.315, wspace=0.2)
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()

# Call the function with the sample image
graph('sample1.png')
