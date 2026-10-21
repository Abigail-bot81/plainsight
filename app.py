optimized_image_bytes = optimize_uploaded_image(uploaded_file)
    image_part = types.Part.from_bytes(
        data=optimized_image_bytes, mime_type="image/jpeg"
    )

    analysis_text = ""
    error_message = ""

    candidate_models = ["gemini-2.5-flash", "gemini-flash-latest"]

    # Retry parameters for handling temporary 503 traffic spikes
    max_retries = 3

    for model_name in candidate_models:
      success = False
      for attempt in range(max_retries):
        try:
          config = types.GenerateContentConfig(
              max_output_tokens=300, temperature=0.3
          )
          response_stream = client.models.generate_content_stream(
              model=model_name, contents=[prompt, image_part], config=config
          )
          temp_text = ""
          for chunk in response_stream:
            if hasattr(chunk, "text") and chunk.text:
              temp_text += chunk.text
              live_placeholder.markdown(temp_text)

          if temp_text:
            analysis_text = temp_text
            success = True
            break  # Success on this model! Exit retry loop
        except Exception as e:
          error_message = str(e)
          # If it's a 503 or overload, wait a bit longer before retrying (exponential backoff)
          wait_time = (attempt + 1) * 1.5
          time.sleep(wait_time)
          continue

      if success:
        break  # Exit model selection loop if we got our result
