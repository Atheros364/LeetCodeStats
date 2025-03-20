# LeetCodeStats

A tool to track and analyze your LeetCode statistics and progress.

## Setup

### Authentication

This tool uses LeetCode's GraphQL API which requires authentication. To set up authentication:

1. Log in to your LeetCode account in your web browser
2. Open Developer Tools (F12 or right-click -> Inspect)
3. Go to the Application/Storage tab
4. Under Cookies, find the cookie for leetcode.com
5. Look for the `LEETCODE_SESSION` cookie and copy its value
6. Create a `.env` file in the project root with the following content:
   ```
   LEETCODE_SESSION=your_cookie_value_here
   ```

The session token will remain valid as long as you don't log out in your browser. If the token expires, you'll need to get a new one and update the `.env` file.

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
LEETCODE_SESSION=your_session_token_here
```

## Usage

[Add usage instructions here]

## Development

[Add development instructions here]