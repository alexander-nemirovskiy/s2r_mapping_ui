import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'confidenceScore'})
export class ConfidenceScorePipe implements PipeTransform {
    transform(value: number): string{
        if (value >= 8){
            return 'High confidence';
        }
        else if (value < 8 && value >= 3){
            return 'Medium confidence';
        }
        return 'Low confidence';
    }
}