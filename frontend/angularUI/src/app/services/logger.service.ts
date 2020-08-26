import { environment } from './../../environments/environment';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LoggerService {

    constructor() { }

    log(msg: any)   {
        if (!environment.production){
            console.log(msg);
        }
    }



    error(msg: any) { console.error(msg); }
    warn(msg: any)  { console.warn(msg); }
}
