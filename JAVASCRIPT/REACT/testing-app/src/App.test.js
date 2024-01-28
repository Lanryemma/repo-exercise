import { fireEvent, render, screen } from '@testing-library/react';
import FeeedBackForm from './FeeedBackForm';


describe("FeedBack Form Test",()=>{
  test('if Submission is disabled and score is less than 5 and comment is less than 10 char', () => {
    const FinalSubmit = jest.fn()
    render(<FeeedBackForm onSubmit={FinalSubmit} />);

    const rangeInput = screen.getByLabelText(/Score:/);
    fireEvent.change(rangeInput,{ target: { value: "4"} });

    const submitButton = screen.getByRole("button");
    fireEvent.click(submitButton);
   
    expect(FinalSubmit).not.toHaveBeenCalled();
    expect(submitButton).toHaveAttribute("disabled");
  });

  test("User is able to submit the form if the score is lower than 5 and additional feedback is provided", () => {
    const score = "3";
    const comment = "The pizza crust was too thick";
    const FinalSubmit = jest.fn();
    render(<FeeedBackForm onSubmit={FinalSubmit} />);

    const rangeInput = screen.getByLabelText(/Score:/);
    fireEvent.change(rangeInput, { target: { value: score } });

    const textArea = screen.getByLabelText(/comments:/);
    fireEvent.change(textArea, { target: { value: comment } });

    const submitButton = screen.getByRole("button");
    fireEvent.click(submitButton);

    expect(FinalSubmit).toHaveBeenCalledWith({
      score,
      comment,
    });
  });

  test("User is able to submit the form if the score is higher than 5, without additional feedback", () => {
    const score = "9";
    const handleSubmit = jest.fn();
    render(<FeeedBackForm onSubmit={handleSubmit} />);

    const rangeInput = screen.getByLabelText(/Score:/);
    fireEvent.change(rangeInput, { target: { value: score } });

    const submitButton = screen.getByRole("button");
    fireEvent.click(submitButton);

    expect(handleSubmit).toHaveBeenCalledWith({
      score,
      comment: "",
    });
  });
})
