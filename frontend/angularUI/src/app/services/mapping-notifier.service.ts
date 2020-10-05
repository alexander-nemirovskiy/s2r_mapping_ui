import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { ChosenFiles } from '../models/MappingPair';
import { LoggerService } from './logger.service';

@Injectable({
  providedIn: 'root'
})
export class MappingNotifierService {

    private subject$ = new BehaviorSubject<ChosenFiles>(null);
    public notification$ = this.subject$.asObservable();

    constructor(private logger: LoggerService) { }

    notify(sourceName: string, targetName: string){
        this.logger.log(`Started mapping invocation using chosen files: \n${sourceName} - ${targetName}`);
        this.subject$.next(new ChosenFiles(sourceName, targetName))
    }
}
