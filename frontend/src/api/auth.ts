// Calls to the backend's auth endpoints.
// TODO: the Django backend has no auth endpoints yet. Until it does, these
// pretend to succeed. When they exist, send the request and throw an
// AuthError with one of the messages below for the matching failure.

export class AuthError extends Error {}

export const WRONG_PASSWORD = 'Wrong email or password.'
export const EMAIL_TAKEN = 'An account with this email already exists.'

export async function login(email: string, password: string): Promise<void> {
  void email
  void password
}

export async function register(
  name: string,
  email: string,
  password: string,
): Promise<void> {
  void name
  void email
  void password
}
