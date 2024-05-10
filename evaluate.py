from rouge_score import rouge_scorer

# Example generated and reference summaries
generated_summary = "John Doe has a booked appointment on May 15, 2024 from 10:00 AM to 10:30 AM at General Hospital with Dr. Jane Smith for a regularly scheduled walk-in visit. The appointment is for a general practice check-up and was created on May 10, 2024."
reference_summary = "John Doe has a booked appointment for a regular check-up with Dr. Jane Smith at General Hospital on May 15th, 2024, from 10:00 AM to 10:30 AM. This appointment was created on May 10th, 2024, and it's marked as required for both the patient and the practitioner. The patient is due for a routine examination."

# Initialize ROUGE scorer
scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)

# Calculate ROUGE scores
scores = scorer.score(generated_summary, reference_summary)

# Print ROUGE scores
print("ROUGE-1 Precision:", scores['rouge1'].precision)
print("ROUGE-1 Recall:", scores['rouge1'].recall)
print("ROUGE-1 F1 Score:", scores['rouge1'].fmeasure)
