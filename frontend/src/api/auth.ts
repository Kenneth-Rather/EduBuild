// Placeholder login with DB - Jacklyn and Dylan

// Calls to the backend's auth endpoints.
// TODO: the Django backend has no auth endpoints yet. Until it does, these
// pretend to succeed. When they exist, send the request and throw an
// AuthError with one of the messages below for the matching failure.

export class AuthError extends Error {}

export const WRONG_PASSWORD = 'Wrong email or password.'
export const EMAIL_TAKEN = 'An account with this email already exists.'

const USERNAME_KEY = 'edubuild-database-username'

function rememberUsername(username: string) {
  try {
    localStorage.setItem(USERNAME_KEY, username)
  } catch {
    // Saving a username is optional for the prototype.
  }
}

export function getStoredUsername(): string {
  try {
    return localStorage.getItem(USERNAME_KEY) ?? 'demo_user'
  } catch {
    return 'demo_user'
  }
}

export async function login(email: string, password: string): Promise<void> {
  void password
  rememberUsername(email.trim())
}

export async function register(
  name: string,
  email: string,
  password: string,
): Promise<void> {
  void email
  void password
  rememberUsername(name.trim() || email.trim())
}
