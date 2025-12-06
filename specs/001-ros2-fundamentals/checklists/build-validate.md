# Module 1: ROS 2 Fundamentals - Build Validation Checklist

This checklist outlines the steps to build all ROS 2 example packages within Module 1 and verify their compilation status.

## Prerequisites

-   A functional ROS 2 Humble Hawksbill installation.
-   A ROS 2 workspace (e.g., `~/ros2_ws`) with all module example packages (`rclpy_examples`, `service_examples`, `urdf_examples`, `launch_examples`, and any custom packages from Capstone) cloned into its `src` directory.

## Build Steps

1.  **Navigate to Workspace Root:**
    ```bash
    cd ~/ros2_ws # Or your workspace root
    ```

2.  **Clean Previous Builds (Optional but Recommended):**
    ```bash
    rm -rf build install log
    ```

3.  **Perform Colcon Build:**
    ```bash
    colcon build
    ```

    *Expected Output:* The build process should complete without errors. You should see output indicating successful compilation and installation of all packages. Look for messages like `[rclpy_examples finished]`.

## Verification Checklist

-   [ ] **All Packages Built Successfully:** Check the `colcon build` output to ensure no packages failed to build.
-   [ ] **Executable Files Generated:** Verify that executables and Python scripts are installed in the `install/<package_name>/lib/<package_name>/` directories (e.g., `install/pub_sub_demo/lib/pub_sub_demo/minimal_publisher`).
-   [ ] **`install/setup.bash` Exists:** Confirm that the workspace setup file is present, which is crucial for sourcing the environment.
-   [ ] **No Warnings/Errors (Critical):** Review the build log for any critical warnings or errors that might indicate potential runtime issues.

## Troubleshooting Build Issues

-   **Missing Dependencies:** If `colcon build` fails due to missing packages, ensure all `depend` entries in your `package.xml` files are correctly specified and that you have installed the corresponding ROS 2 packages (e.g., `sudo apt install ros-humble-rclpy ros-humble-std-msgs`).
-   **Python Syntax Errors:** Check Python scripts for syntax errors. `ament_flake8` and `ament_pep257` tests (run during `colcon test`) can help identify style and basic syntax issues.
-   **CMake/ament_python Errors:** Ensure your `CMakeLists.txt` (if any, for C++ packages) and `setup.py` are correctly configured according to ROS 2 package guidelines.

## Smoke Test Results (2025-12-06)

### Docusaurus Build (`npm run build --prefix docusaurus-project`)
- **Status:** SUCCESS with WARNINGS
- **Warnings:**
    - No docs found in "module-1-ros2": can't auto-generate a sidebar.
    - Docusaurus found broken links, specifically to `/docs/module-1-ros2-introduction` across multiple pages.

### ROS 2 Colcon Build (`colcon build --packages-select pub_sub_demo service_action_demo urdf_examples`)
- **Status:** FAILED
- **Error:** `colcon: command not found`. This indicates that the ROS 2 environment is not properly sourced or `colcon` is not installed/available in the system's PATH.
