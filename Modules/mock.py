import streamlit as st  # type: ignore

def app():
    st.title("NEET Exam Mock Test Site")

    st.write("### Mock Test Guidelines")
    st.write(
        """
        For conducting a mock test for your final year project, considering the parameters you've mentioned, here are the guidelines you can follow:
        1. Duration: Allocate 3 hours of time for the mock test, mirroring the actual NEET exam duration.

        2. Total Marks: Set the total marks for the mock test to 720, aligning with the NEET exam's total marks.

        3. Question Format: Design the mock test with a variety of question formats, including multiple-choice questions, match the following, assertion-reasoning, etc., similar to the NEET exam pattern.

        4. Negative Marking: Implement negative marking of 1/4 for incorrect answers to simulate the NEET exam's marking scheme accurately.

        5. Question Distribution: Distribute the questions across the relevant subjects, such as Physics, Chemistry, and Biology, according to the NEET syllabus.

        6. Difficulty Level: Ensure that the difficulty level of the questions reflects that of the actual NEET exam, with some easy, moderate, and challenging questions.

        7. Instructions: Provide clear instructions to the participants regarding the rules of the mock test, including the marking scheme, time allocation, and any specific guidelines.

        8. Mock Test Platform: Choose a suitable platform or method for administering the mock test, whether it's through an online portal, paper-based format, or any other means feasible for your project.

        9. Analysis and Evaluation: Analyze the results of the mock test to assess the effectiveness of your project in simulating the NEET exam experience and identify any areas for refinement or enhancement.

        By following these guidelines, you can effectively conduct a mock test for your final year project, providing valuable insights into the participants' preparedness for the actual NEET exam.
        """
    )


if __name__ == "__main__":
    app()
