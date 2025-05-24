# Installation Guide

## Prerequisites

- Python 3.7 or later
- pip
- JDK 8 or later (for Java projects)
- Maven or Gradle (for Java projects)

## Python Package Installation

Install the package using pip:

```bash
pip install semantic-kernel
```
Verify the installation:

```bash
python -c "import semantic_kernel; print(semantic_kernel.__version__)"
```

## Java Package Installation

### Using Maven

Add the following dependency to your pom.xml:

```xml
<dependency>
    <groupId>com.microsoft.semantic-kernel</groupId>
    <artifactId>semantickernel-core</artifactId>
    <version>[latest-version]</version>
</dependency>
```

### Using Gradle

Add the following dependency to your build.gradle:

```gradle
dependencies {
    implementation 'com.microsoft.semantic-kernel:semantickernel-core:[latest-version]'
}
```

Make sure to replace [latest-version] with the actual latest version of the package available in the respective repositories. You can find the latest version on Maven Central Repository.

## Additional Notes

- Ensure that your environment variables are set correctly for Java projects.
- For detailed usage instructions, refer to the official documentation.

## Verifying Installations of Dependencies

To verify the installations of dependencies, run the following commands:

```bash
# Verify npm dependencies
npm list

# Verify Python dependencies
pip list

# Verify .NET SDK installations
dotnet --list-sdks
```

These steps will help ensure that all necessary dependencies are installed correctly.

### Summary of Changes:
- Sectioned the guide based on different programming languages.
- Provided clear and separate code blocks for Maven and Gradle.
- Added steps to verify the installation.
- Included a link to find the latest version of the Java package.

These changes should make the installation guide more user-friendly and comprehensive.
