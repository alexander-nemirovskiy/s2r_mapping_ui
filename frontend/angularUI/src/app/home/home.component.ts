import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { Subscription } from 'rxjs';

import { MappingContainerComponent } from '../mapping-container/mapping-container.component';
import { APIError } from '../models/Errors';
import { LoggerService } from '../services/logger.service';
import { MappingNotifierService } from '../services/mapping-notifier.service';

@Component({
    selector: 'home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {
    private sub: Subscription;

    private mappingContainer: MappingContainerComponent;
    @ViewChild(MappingContainerComponent, { static: false }) set content(content: MappingContainerComponent) {
        if (content) {
            // initially setter gets called with undefined
            this.mappingContainer = content;
        }
    }

    public showMappingChild = true;
    public mapping_error = false;
    public process_error = '';

    constructor(
        private notifier: MappingNotifierService,
        private logger: LoggerService) { }

    ngOnInit(): void {
        this.sub = this.notifier.notification$.subscribe(
            message => {
                if (message && !this.showMappingChild) {
                    this.logger.dir(`Dir child component:\n${this.mappingContainer}`);
                    this.showMappingChild = true;
                }
            }
        );
    }

    onEndMapping($event) {
        this.logger.warn('Destroying component');
        this.showMappingChild = false;
        if( $event instanceof APIError){
            this.mapping_error = true;
            this.process_error = $event.message;
        }
    }

    ngOnDestroy(): void {
        this.sub.unsubscribe();
    }
}
