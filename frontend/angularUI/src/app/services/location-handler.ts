import { environment } from 'src/environments/environment';

export function getBaseLocation(): string{
    if(!environment.production)
        return `${location.protocol}//${location.hostname}:5050`;
    return location.origin;
}