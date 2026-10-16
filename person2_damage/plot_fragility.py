from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

xml_path = (
    PROJECT_ROOT
    / "demos"
    / "risk"
    / "ScenarioDamage"
    / "structural_fragility_model.xml" #Using the structural fragility model xml file from the ScenarioDamage demo
)

import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

# Read the fragility XML file
root = ET.parse(xml_path).getroot()

# OpenQuake NRML namespace
ns = {"n": "http://openquake.org/xmlns/nrml/0.5"}

# Find the Wood fragility function
for func in root.findall(".//n:fragilityFunction", ns):

    if func.get("id") != "Adobe":
        continue

    # Read PGA intensity levels
    imls = func.find("n:imls", ns)
    pga_values = [float(x) for x in imls.text.split()]

    # Plot probability of exceeding each damage threshold
    for poes in func.findall("n:poes", ns):
        probabilities = [float(x) * 100 for x in poes.text.split()]

        plt.plot(
            pga_values,
            probabilities,
            marker="o",
            label=poes.get("ls")
        )

plt.xlabel("Peak Ground Acceleration (g)")
plt.ylabel("Probability of Exceedance (%)")
plt.title("Adobe Building Fragility Curves - Nepal Demo")
plt.ylim(0, 100)
plt.legend()
plt.grid(True)

# Save graph into your person2_damage folder
output_path = Path(__file__).resolve().parent / "adobe_fragility.png"
plt.savefig(output_path, dpi=200, bbox_inches="tight")

plt.show()