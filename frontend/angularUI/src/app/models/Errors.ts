export class APIError {
    constructor(public status_code: string,
                public detail: object,
                public code: string = "",
                public message: string = ""){}
}