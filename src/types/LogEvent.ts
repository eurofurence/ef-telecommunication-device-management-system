/**
 * Definition of an event log item
 */
export type LogEvent = {
    id: number;
    date: string;
    type: LogEventType;
    message: string;
    description?: string;
}

export type LogEventType = {
    key: string;
    label: string;
    color: string;
    icon: string;
}
