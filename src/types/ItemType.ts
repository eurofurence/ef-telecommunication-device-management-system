/**
 * Definition of all metadata associated with ItemTypes
 */
export type ItemTypeMetadata = {
    key: string;
    label: string;
    shortLabel: string;
    icon: string;
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
    };

    public static RadioAccessory: ItemTypeMetadata = {
        key: 'RadioAccessory',
        label: 'Radio Accessory',
        shortLabel: 'Accessory',
        icon: 'mdi-headset'
    };

    public static Pager: ItemTypeMetadata = {
        key: 'Pager',
        label: 'Pager',
        shortLabel: 'Pager',
        icon: 'mdi-bell-ring-outline'
    };

    public static Phone: ItemTypeMetadata = {
        key: 'Phone',
        label: 'Phone',
        shortLabel: 'Phone',
        icon: 'mdi-phone'
    };

    public static Callbox: ItemTypeMetadata = {
        key: 'Callbox',
        label: 'Callbox',
        shortLabel: 'Callbox',
        icon: 'mdi-webcam'
    };

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
