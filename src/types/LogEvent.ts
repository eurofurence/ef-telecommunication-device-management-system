/**
 * Definition of an event log item
 */
export type LogEvent = {
    id: number;
    date: string;
    user: string;
    type: LogEventTypeDeclaration;
    message: string;
    description: string;
}

/**
 * Interface contract for LogEventType class
 */
type LogEventTypeDeclaration = {
    key: string;
    label: string;
    color: string;
    icon: string;
    description(data: any): string;
}

/**
 * Log event types
 */
export class LogEventType {

    static readonly USER_LOGIN: LogEventTypeDeclaration = {
        key: 'USER_LOGIN',
        label: 'User logged in',
        color: 'purple-lighten-2',
        icon: 'mdi-login',
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        description(data: any): string {
            return ``;
        }
    }

    static readonly CREATE_ITEM_OWNER: LogEventTypeDeclaration = {
        key: 'CREATE_ITEM_OWNER',
        label: 'Item owner created',
        color: 'green-lighten-1',
        icon: 'mdi-head-plus-outline',
        description(data: any): string {
            return `${data.name} (${data.shortname})`;
        }
    }

    static readonly DELETE_ITEM_OWNER: LogEventTypeDeclaration = {
        key: 'DELETE_ITEM_OWNER',
        label: 'Item owner deleted',
        color: 'red-lighten-1',
        icon: 'mdi-head-remove-outline',
        description(data: any): string {
            return `${data.name} (${data.shortname})`;
        }
    }

    static readonly UPDATE_ITEM_OWNER: LogEventTypeDeclaration = {
        key: 'UPDATE_ITEM_OWNER',
        label: 'Item owner updated',
        color: 'orange-darken-1',
        icon: 'mdi-head-outline',
        description(data: any): string {
            return `${data.name} (${data.shortname})`;
        }
    }

    static readonly CREATE_ITEM: LogEventTypeDeclaration = {
        key: 'CREATE_ITEM',
        label: 'Item created',
        color: 'green-lighten-1',
        icon: 'mdi-plus',
        description(data: any): string {
            return `${data.pretty_name}`;
        }
    }

    static readonly DELETE_ITEM: LogEventTypeDeclaration = {
        key: 'DELETE_ITEM',
        label: 'Item deleted',
        color: 'red-lighten-1',
        icon: 'mdi-minus',
        description(data: any): string {
            return `${data.pretty_name}`;
        }
    }

    static readonly UPDATE_ITEM: LogEventTypeDeclaration = {
        key: 'UPDATE_ITEM',
        label: 'Item updated',
        color: 'orange-darken-1',
        icon: 'mdi-pencil',
        description(data: any): string {
            return `${data.pretty_name}`;
        }
    }

    static readonly CREATE_ITEM_TEMPLATE: LogEventTypeDeclaration = {
        key: 'CREATE_ITEM_TEMPLATE',
        label: 'Item template created',
        color: 'green-lighten-1',
        icon: 'mdi-toy-brick-plus-outline',
        description(data: any): string {
            return `${data.pretty_name}`;
        }
    }

    static readonly DELETE_ITEM_TEMPLATE: LogEventTypeDeclaration = {
        key: 'DELETE_ITEM_TEMPLATE',
        label: 'Item template deleted',
        color: 'red-lighten-1',
        icon: 'mdi-toy-brick-remove-outline',
        description(data: any): string {
            return `${data.pretty_name}`;
        }
    }

    static readonly UPDATE_ITEM_TEMPLATE: LogEventTypeDeclaration = {
        key: 'UPDATE_ITEM_TEMPLATE',
        label: 'Item template updated',
        color: 'orange-darken-1',
        icon: 'mdi-toy-brick-outline',
        description(data: any): string {
            return `${data.pretty_name}`;
        }
    }

    static readonly CREATE_ITEM_BINDING: LogEventTypeDeclaration = {
        key: 'CREATE_ITEM_BINDING',
        label: 'Item binding created',
        color: 'green-lighten-1',
        icon: 'mdi-basket-plus-outline',
        description(data: any): string {
            return `${data.item.pretty_name} to ${data.user.pretty_name}`;
        }
    }

    static readonly DELETE_ITEM_BINDING: LogEventTypeDeclaration = {
        key: 'DELETE_ITEM_BINDING',
        label: 'Item binding deleted',
        color: 'red-lighten-1',
        icon: 'mdi-basket-minus-outline',
        description(data: any): string {
            return `${data.item.pretty_name} from ${data.user.pretty_name}`;
        }
    }

    static readonly UPDATE_ITEM_BINDING: LogEventTypeDeclaration = {
        key: 'UPDATE_ITEM_BINDING',
        label: 'Item binding updated',
        color: 'orange-darken-1',
        icon: 'mdi-basket-outline',
        description(data: any): string {
            return `${data.item.pretty_name} to ${data.user.pretty_name}`;
        }
    }

    static readonly CREATE_ORDER: LogEventTypeDeclaration = {
        key: 'CREATE_ORDER',
        label: 'Order created',
        color: 'green-lighten-1',
        icon: 'mdi-receipt-text-plus',
        description(data: any): string {
            return `${data.title} for ${data.user.pretty_name}`;
        }
    }

    static readonly DELETE_ORDER: LogEventTypeDeclaration = {
        key: 'DELETE_ORDER',
        label: 'Order deleted',
        color: 'red-lighten-1',
        icon: 'mdi-receipt-text-minus',
        description(data: any): string {
            return `${data.title} for ${data.user.pretty_name}`;
        }
    }

    static readonly UPDATE_ORDER: LogEventTypeDeclaration = {
        key: 'UPDATE_ORDER',
        label: 'Order updated',
        color: 'orange-darken-1',
        icon: 'mdi-receipt-text-edit',
        description(data: any): string {
            return `${data.title} for ${data.user.pretty_name}`;
        }
    }

    static readonly CREATE_RADIO_CODING: LogEventTypeDeclaration = {
        key: 'CREATE_RADIO_CODING',
        label: 'Radio coding created',
        color: 'green-lighten-1',
        icon: 'mdi-plus',
        description(data: any): string {
            return `Name: ${data.name}`;
        }
    }

    static readonly DELETE_RADIO_CODING: LogEventTypeDeclaration = {
        key: 'DELETE_RADIO_CODING',
        label: 'Radio coding deleted',
        color: 'red-lighten-1',
        icon: 'mdi-minus',
        description(data: any): string {
            return `Name: ${data.name}`;
        }
    }

    static readonly UPDATE_RADIO_CODING: LogEventTypeDeclaration = {
        key: 'UPDATE_RADIO_CODING',
        label: 'Radio coding updated',
        color: 'orange-darken-1',
        icon: 'mdi-pencil',
        description(data: any): string {
            return `Name: ${data.name}`;
        }
    }

    static readonly UNKNOWN: LogEventTypeDeclaration = {
        key: 'UNKNOWN',
        label: 'Unknown',
        color: 'grey',
        icon: 'mdi-help',
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        description(data: any): string {
            return 'Unknown event';
        }
    }

    /**
     * Returns the LogEventTypeDeclaration for the given key or UNKNOWN
     *
     * @param key of the LogEventType
     * @return LogEventTypeDeclaration for the given key
     */
    static get(key: string): LogEventTypeDeclaration {
        return <LogEventTypeDeclaration>LogEventType[key as keyof typeof LogEventType] ?? LogEventType.UNKNOWN;
    }

    /**
     * Returns all existing LogEventTypes
     */
    static getAll(): LogEventTypeDeclaration[] {
        return Object.values(this).filter(obj => obj.key) as LogEventTypeDeclaration[];
    }

}