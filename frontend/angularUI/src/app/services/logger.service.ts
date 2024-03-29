import { Injectable } from '@angular/core';
import { environment } from './../../environments/environment';

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
    
    dir(msg: any)   {
        if (!environment.production){
            console.dir(msg);
        }
    }

    error(msg: any) { console.error(msg); }
    warn(msg: any)  { 
        if (!environment.production){
            console.warn(msg);
        }
    }
}
