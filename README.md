# SIMPSON GUI

---

## Overview
The **SIMPSON GUI** project provides a streamlined Graphical User Interface (GUI), created using Streamlit, to simplify the creation of SIMPSON files for NMR simulations.
By using this interface, you can generate SIMPSON input files.

---

## Installation and Usage

### Prerequisites

1. Install **[Streamlit](https://docs.streamlit.io/get-started/installation)**.
2. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/dnp-grenoble/simpson_gui.git
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Navigate to the project directory.
2. Launch the application using **Streamlit**:
   ```bash
   streamlit run Homepage.py
   ```

---

## Features
- User-friendly interface to configure and generate SIMPSON files.
- Integrated utilities for handling `xyz` files and dipolar couplings.
- Customizable settings for execution methods and propagation techniques.
- Helpful tools to configure optimal verbosity levels for simulations.

For additional details, please refer to the functionality described in `Homepage.py`.
More pulse sequences will be added in due course.

---

## Contribution
Contributions are welcome! Please feel free to submit issues or pull requests to enhance the project.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Support
For further help, please open an issue in the repository or consult the documentation linked within the app.