import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { LoggerService } from './logger.service';

@Injectable({
  providedIn: 'root'
})
export class MappingNotifierService {

    private subject$ = new Subject<boolean>();
    public notification = this.subject$.asObservable();

    constructor(private logger: LoggerService) { }

    notify(){
        this.logger.log('Started mapping invocation');
        this.subject$.next(true)
    }
}
