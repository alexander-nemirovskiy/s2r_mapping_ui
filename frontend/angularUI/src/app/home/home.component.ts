import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { Subscription } from 'rxjs';

import { MappingContainerComponent } from '../mapping-container/mapping-container.component';
import { LoggerService } from '../services/logger.service';
import { MappingNotifierService } from '../services/mapping-notifier.service';

@Component({
    selector: 'home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {
    private mappingContainer: MappingContainerComponent;
    @ViewChild(MappingContainerComponent, { static: false }) set content(content: MappingContainerComponent) {
        if (content) {
            // initially setter gets called with undefined
            this.mappingContainer = content;
        }
    }

    public showMappingChild = true;
    private sub: Subscription;

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
    }

    ngOnDestroy(): void {
        this.sub.unsubscribe();
    }
}
