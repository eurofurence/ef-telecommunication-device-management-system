/**
 * Definition of all metadata associated with ItemTypes
 */
export type ItemTypeMetadata = {
    key: string;
    label: string;
    shortLabel: string;
    icon: string;
    color: string;
}

/**
 * All available item types
 */
export class ItemType {

    public static RadioDevice: ItemTypeMetadata = {
        key: 'RadioDevice',
        label: 'Radio Device',
        shortLabel: 'Radio',
        icon: 'mdi-cellphone-basic',
        color: '#1E88E5',
    };

    public static RadioAccessory: ItemTypeMetadata = {
        key: 'RadioAccessory',
        label: 'Radio Accessory',
        shortLabel: 'Accessory',
        icon: 'mdi-headset',
        color: '#00ACC1',
    };

    public static Pager: ItemTypeMetadata = {
        key: 'Pager',
        label: 'Pager',
        shortLabel: 'Pager',
        icon: 'mdi-bell-ring-outline',
        color: '#26A69A',
    };

    public static Phone: ItemTypeMetadata = {
        key: 'Phone',
        label: 'Phone',
        shortLabel: 'Phone',
        icon: 'mdi-phone',
        color: '#D4E157',
    };

    public static Callbox: ItemTypeMetadata = {
        key: 'Callbox',
        label: 'Callbox',
        shortLabel: 'Callbox',
        icon: 'mdi-webcam',
        color: '#6D4C41',
    };

    public static Unknown: ItemTypeMetadata = {
        key: 'Unknown',
        label: 'Unknown',
        shortLabel: 'Unknown',
        icon: 'mdi-help-circle',
        color: '#BDBDBD'
    }

    /**
     * Returns the ItemTypeMetadata for the given key or UNKNOWN
     *
     * @param key of the LogEventType
     * @return LogEventTypeDeclaration for the given key
     */
    static get(key: string): ItemTypeMetadata {
        return <ItemTypeMetadata>ItemType[key as keyof typeof ItemType] ?? ItemType.Unknown;
    }

    /**
     * Retrieves all available item types
     */
    public static getAll(): ItemTypeMetadata[] {
        return [
            ItemType.RadioDevice,
            ItemType.RadioAccessory,
            ItemType.Pager,
            ItemType.Phone,
            ItemType.Callbox
        ];
    }

}

/**
 * Definition of all metadata associated with ItemTemplateTypes
 */
export type ItemTemplateTypeMetadata = {
    key: string;
    itemType: ItemTypeMetadata;
}

/**
 * All available item template types
 */
export class ItemTemplateType {

    public static RadioDeviceTemplate: ItemTemplateTypeMetadata = {
        key: 'RadioDeviceTemplate',
        itemType: ItemType.RadioDevice
    };

    public static RadioAccessoryTemplate: ItemTemplateTypeMetadata = {
        key: 'RadioAccessoryTemplate',
        itemType: ItemType.RadioAccessory
    };

    public static PagerTemplate: ItemTemplateTypeMetadata = {
        key: 'PagerTemplate',
        itemType: ItemType.Pager
    };

    public static PhoneTemplate: ItemTemplateTypeMetadata = {
        key: 'PhoneTemplate',
        itemType: ItemType.Phone
    };

    public static CallboxTemplate: ItemTemplateTypeMetadata = {
        key: 'CallboxTemplate',
        itemType: ItemType.Callbox
    };

    public static UnknownTemplate: ItemTemplateTypeMetadata = {
        key: 'UnknownTemplate',
        itemType: ItemType.Unknown
    }

    /**
     * Returns the ItemTypeMetadata for the given key or UNKNOWN
     *
     * @param key of the LogEventType
     * @return LogEventTypeDeclaration for the given key
     */
    static get(key: string): ItemTemplateTypeMetadata {
        return <ItemTemplateTypeMetadata>ItemTemplateType[key as keyof typeof ItemTemplateType] ?? ItemTemplateType.UnknownTemplate;
    }

    /**
     * Retrieves all available item template types
     */
    public static getAll(): ItemTemplateTypeMetadata[] {
        return [
            ItemTemplateType.RadioDeviceTemplate,
            ItemTemplateType.RadioAccessoryTemplate,
            ItemTemplateType.PagerTemplate,
            ItemTemplateType.PhoneTemplate,
            ItemTemplateType.CallboxTemplate
        ];
    }

}
