import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';
import { LoggerService } from './logger.service';

@Injectable({
  providedIn: 'root'
})
export class MappingNotifierService {

    private subject$ = new BehaviorSubject<boolean>(null);
    public notification$ = this.subject$.asObservable();

    constructor(private logger: LoggerService) { }

    notify(){
        this.logger.log('Started mapping invocation');
        this.subject$.next(true)
    }
}
