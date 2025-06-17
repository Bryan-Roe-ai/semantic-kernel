/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

export class AzureLoginError extends Error {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/explicit-module-boundary-types
  constructor(message: string, public reason?: any) {
    super(message);
    this.name = "AzureLoginError";

    // Maintain proper prototype chain for instanceof checks
    Object.setPrototypeOf(this, AzureLoginError.prototype);
  }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/explicit-module-boundary-types
export function getErrorMessage(err: any): string | undefined {
  if (!err) {
    return;
  }

  /* eslint-disable @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return */
  if (err.message && typeof err.message === "string") {
    return err.message;
  }

  if (err.stack && typeof err.stack === "string") {
    // eslint-disable-next-line  @typescript-eslint/no-unsafe-call
    return err.stack.split("\n")[0];
  }

  const str = String(err);
  if (!str || str === "[object Object]") {
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
    const ctr = err.constructor;
    if (ctr && ctr.name && typeof ctr.name === "string") {
      return ctr.name;
    }
    return "Unknown error";
  }
  /* eslint-enable @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return */

  return str;
}

export class AzureConfigurationError extends Error {
  constructor(message: string, public configKey?: string) {
    super(message);
    this.name = "AzureConfigurationError";
    Object.setPrototypeOf(this, AzureConfigurationError.prototype);
  }
}

export class AzureConnectionError extends Error {
  constructor(
    message: string,
    public endpoint?: string,
    public statusCode?: number
  ) {
    super(message);
    this.name = "AzureConnectionError";
    Object.setPrototypeOf(this, AzureConnectionError.prototype);
  }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function isAzureError(
  err: any
): err is AzureLoginError | AzureConfigurationError | AzureConnectionError {
  return (
    err instanceof AzureLoginError ||
    err instanceof AzureConfigurationError ||
    err instanceof AzureConnectionError
  );
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function sanitizeError(err: any): {
  message: string;
  type: string;
  details?: any;
} {
  const message = getErrorMessage(err) || "An unknown error occurred";

  if (err instanceof AzureLoginError) {
    return {
      message,
      type: "AzureLoginError",
      details: err.reason ? { reason: err.reason } : undefined,
    };
  }

  if (err instanceof AzureConfigurationError) {
    return {
      message,
      type: "AzureConfigurationError",
      details: err.configKey ? { configKey: err.configKey } : undefined,
    };
  }

  if (err instanceof AzureConnectionError) {
    return {
      message,
      type: "AzureConnectionError",
      details: {
        endpoint: err.endpoint,
        statusCode: err.statusCode,
      },
    };
  }

  return {
    message,
    type: err.constructor?.name || "Error",
  };
}
