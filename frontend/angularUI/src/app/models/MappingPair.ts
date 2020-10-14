export class MappingPair {
    constructor (
        public sourceTerm: string,
        public mappingOptions: string[],
        public confidenceScores: number[]
    ) {}
}

export class ChosenFiles {
    constructor (
        public sourceName: string,
        public targetName: string
    ){}
}