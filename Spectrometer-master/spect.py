import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Updated element ranges
elements = {
    'Albite': [400, 500],
    'Azurite': [600, 700],
    'Beryl': [400, 500],
    'Biotite': [500, 600],
    'Calcite': [400, 450],
    'Chalcopyrite': [500, 700],
    'Chlorite': [500, 550],
    'Copper': [600, 700],
    'Epidote': [450, 550],
    'Goethite': [480],
    'Gypsum': [450, 500],
    'Hematite': [450],
    'Iron': [400, 500],
    'Kaolinite': [450, 500],
    'Limonite': [500],
    'Magnetite': [400, 700],
    'Malachite': [600, 700],
    'Manganese': [500, 600],
    'Muscovite': [450, 550],
    'Olivine': [400, 500],
    'Orthoclase': [400, 450],
    'Pyrite': [500, 600],
    'Quartz': [400, 500],
    'Rutile': [400, 450],
    'Siderite': [400, 500],
    'Vermiculite': [450, 500],
    'Zinc': [500, 600]
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
