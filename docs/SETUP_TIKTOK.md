# Connect a TikTok account

This is the fast owner-account path for TikTok Display API v2.

## Sandbox bootstrap

1. Sign in at <https://developers.tiktok.com/apps/> and create an app.
2. Create a Sandbox and add the owner TikTok account as a target user.
3. Add Login Kit and TikTok/Display API.
4. Request only `user.info.basic` and `video.list`.
5. Configure an exact HTTPS redirect URI and complete Authorization Code OAuth.
6. Store the resulting access token locally:

   ```bash
   PYTHONPATH=src python -m aoa_tiktok_connector setup --json
   ```

7. Paste it after `AOA_TIKTOK_ACCESS_TOKEN=` in the generated mode-`0600` file,
   never into chat, then validate:

   ```bash
   PYTHONPATH=src python -m aoa_tiktok_connector config-check --json
   PYTHONPATH=src python -m aoa_tiktok_connector auth-check --json
   PYTHONPATH=src python -m aoa_tiktok_connector videos-list --max-count 10 --json
   ```

## Boundaries

- Sandbox allows integration work before Production review.
- Production review requires a developed public website with visible Privacy
  Policy and Terms, verified URLs, and an end-to-end demo video.
- `video.upload` and `video.publish` are not requested in this phase.
- Posting remains disabled even when profile/video reads succeed.

Official sources:

- https://developers.tiktok.com/docs/en/getting-started-create-an-app
- https://developers.tiktok.com/docs/en/add-a-sandbox
- https://developers.tiktok.com/docs/en/display-api-get-started
- https://developers.tiktok.com/docs/en/app-review-guidelines
