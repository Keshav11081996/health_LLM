# Health API

This API allows users to calculate wellness scores, generate health goals, and update wellness scores based on completed goals. It is designed to help users track and improve their physical, mental, social, sleep, and nutritional well-being.

## Features

- **Calculate Wellness Scores**: Computes wellness scores based on various health parameters.
- **Generate Health Goals**: Suggests personalized health goals based on the user's current state.
- **Update Wellness Scores**: Updates scores based on goal completion rates.

## Prerequisites

- Docker installed on your machine.
- A machine with GPU support if needed (optional).

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Build the Docker image:**

   ```bash
   docker build -t health_api .
   ```

3. **Run the Docker container:**

   ```bash
   docker run --gpus all -p 8000:8000 health_api
   ```

## Usage

### 1. Calculate Wellness Scores

To calculate wellness scores, use the following `curl` command:

```bash
curl -X POST "http://localhost:8000/wellness/calculate_scores" \
     -H "Content-Type: application/json" \
     -d '{
           "physical": {
             "steps": 8000,
             "exercise_frequency": 5,
             "hrv": 60
           },
           "mental": {
             "mood": 8,
             "stress_levels": 3,
             "meditation_frequency": 4
           },
           "social": {
             "social_interactions": 7,
             "quality_of_interactions": 9
           },
           "sleep": {
             "sleep_duration": 7,
             "sleep_quality": 8
           },
           "nutrition": {
             "diet_quality": 7,
             "hydration_levels": 90
           },
           "primary_goal": "A"
         }'
```

### 2. Generate Health Goals

To generate health goals based on the user's state, use this `curl` command:

```bash
curl -X POST "http://localhost:8000/goals/generate" \
     -H "Content-Type: application/json" \
     -d '{
  "messages": [
    {
      "role": "user",
      "content": "This is my health state: { \"physical\": { \"steps\": 13000, \"exercise_frequency\": 90, \"hrv\": 60 }, \"mental\": { \"mood\": 8, \"stress_levels\": 70, \"meditation_frequency\": 5 }, \"social\": { \"social_interactions\": 10, \"quality_of_interactions\": 8 }, \"sleep\": { \"sleep_duration\": 7, \"sleep_quality\": 80 }, \"nutrition\": { \"diet_quality\": 80, \"hydration_levels\": 90 }, \"primary_goal\": \"C\" }"
    },
    {
      "role": "assistant",
      "content": "Below is your health score: {\"Physical Wellness Score\":88.0,\"Mental Wellness Score\":74.42857142857143,\"Social Wellness Score\":45.0,\"Sleep Wellness Score\":83.75,\"Nutrition Wellness Score\":84.0,\"Holistic Wellness Score\":72.66883116883118}"
    },
    {
      "role": "user",
      "content": "Given my current mental well-being, can you suggest 2 crisp titled goals with brief descriptions to improve it?"
    }
  ]
}'
```

### 3. Update Wellness Scores

To update the wellness scores after goal completion, use this `curl` command:

```bash
curl -X POST "http://localhost:8000/wellness/update_scores" \
     -H "Content-Type: application/json" \
     -d '{ 
           "initial_scores": { 
             "Physical Wellness Score": 80, 
             "Mental Wellness Score": 90, 
             "Social Wellness Score": 60, 
             "Sleep Wellness Score": 90, 
             "Nutrition Wellness Score": 85 
           }, 
           "last_goal_content": "Completed daily exercise for 30 minutes", 
           "completion_rate": 75.0 
         }'
```

### 4. Heatlh Check

health check get endpoint

```bash
curl -X GET "http://localhost:8000/health/check"      
     -H "Content-Type: application/json"      
```

## API Endpoints

- **`/wellness/calculate_scores`**: POST - Calculate wellness scores based on provided health data.
- **`/goals/generate`**: POST - Generate personalized health goals.
- **`/wellness/update_scores`**: POST - Update wellness scores based on goal completion.