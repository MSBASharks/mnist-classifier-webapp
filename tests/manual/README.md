# Manual Upload Validation Tests

Tester: Andrew Brooks  
Date: September 12, 2026  
Website: https://balcony-lapped-silicon.ngrok-free.dev

## Results

| Test | File | Expected behavior | Actual result | Status |
|---|---|---|---|---|
| Empty CSV | fixtures/empty.csv | Reject the empty file with a clear error. | Displayed “The submitted file is empty.” | Pass |
| Wrong dimensions | fixtures/wrong-size-27x28.csv | Reject an image that is not 28×28. | Displayed “Expected exactly 28 rows, found 27. Check that the file has no header row and isn't missing/extra lines.” | Pass |
| Non-CSV upload | fixtures/non-csv.png | Reject the file type with a clear error. | Displayed “That file is not a CSV. Please upload a .csv file.” | Pass |
| Valid upload after an error | fixtures/sample_data.csv | Display the image and a prediction after rejecting an invalid upload. | Displayed the digit image and predicted 8 with 100.0% confidence shown. | Pass |

## How to Repeat

1. Log in and open the classification page.
2. Upload each file in the order listed above and click Classify.
3. Compare the result with the expected behavior.
4. Confirm that the upload form remains usable after each rejection.

The valid sample_data.csv was provided in the project posting in canvas. The other files were prepared for validation testing.

## Notes and Unresolved Issue

### Error visibility

The wrong-dimensions error appeared above the page heading and was initially overlooked. Make the message more prominent and place it near the upload form.

### Trained model verification

The results page says predictions come from a placeholder stub rather than the trained model. The handoff document says the real model is connected.

This may be outdated page text. Inspect the deployed prediction code to confirm which model is used before changing the warning or claiming that model integration is verified.

## Scope

All four upload tests passed. These results verify the observed file handling, image display, and ability to submit a valid file after an error.

They do not establish model accuracy or confirm that the trained model is being used. The displayed 100.0% confidence is not overall model accuracy.
