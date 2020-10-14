import { Component, OnInit, OnDestroy, Output, EventEmitter } from '@angular/core';
import { SubSink } from 'subsink';

import { MappingNotifierService } from '../services/mapping-notifier.service';
import { LoggerService } from '../services/logger.service';
import { MappingService } from '../services/mapping.service';
import { MappingPair } from '../models/MappingPair';
import { APIError } from '../models/Errors';
import { catchError } from 'rxjs/operators';

@Component({
  selector: 'mapping-container',
  templateUrl: './mapping-container.component.html',
  styleUrls: ['./mapping-container.component.scss']
})
export class MappingContainerComponent implements OnInit, OnDestroy {
    @Output() finalizeMapping: EventEmitter<any> = new EventEmitter();

    visible = false;
    localMappings: MappingPair[];
    confirmedItems: MappingPair[] = [];
    mapping_error: boolean = false;
    mapping_error_message: string = '';
    
    private subs: SubSink = new SubSink();

    constructor(
        private mappingService: MappingService,
        private notifier: MappingNotifierService, 
        private logger: LoggerService) { }

    ngOnInit(): void {
        this.resetErrorField();
        this.subs.add(
            this.notifier.notification$.subscribe(
                message => {
                    this.visible = message ? true: false;
                    this.logger.log('Notification received');
                    this.localMappings = null;
                    this.resetErrorField();
                    if (message && message.sourceName && message.targetName) {
                        this.subs.add(this.mappingService.startMapping(message.sourceName, message.targetName)
                            .pipe(
                                catchError(err => {
                                    this.logger.warn('Error received: propagating')
                                    this.mapping_error = true;
                                    this.mapping_error_message = err.message? err.message: JSON.stringify(err.detail);
                                    throw(err);
                                })
                            )
                            .subscribe(
                                items => { this.localMappings = items; }
                            ));
                    }
                }
            ),
            this.mappingService.confirmedPairs$.subscribe(
                (pair: MappingPair) => {
                    this.logger.log(`Confirmed items count: ${this.confirmedItems.length}`)
                    this.confirmedItems.push(pair);
                }
            )
        );
    }

    finalizeChoice(){
        this.confirmedItems.forEach((item) => {
            console.log(item.sourceTerm)
        })
        this.subs.add(this.mappingService.finalizeMappings(this.confirmedItems)
            .subscribe(
                data => {
                    this.resetErrorField();
                    this.finalizeMapping.emit(this);
                    this.logger.log('Confirmation choices received. Ready to delete')
                },
                error => {
                    this.mapping_error = true;
                    this.mapping_error_message = error.message? error.message: JSON.stringify(error.detail);
                    this.finalizeMapping.emit(error);
                }
            )
        );
    }

    dismissChild($event: MappingPair){
        this.localMappings = this.localMappings.filter(x => x.sourceTerm !== $event.sourceTerm);
    }

    ngOnDestroy(): void {
        this.subs.unsubscribe();
        this.logger.log(`Destroy call made for component ${this}`);
    }

    private resetErrorField(){
        this.mapping_error = false;
        this.mapping_error_message = '';
    }

}
