/* Eurofurence Telecommunication Device Management System (EF-TDMS)
 * Copyright (C) 2025 Niels Gandraß <niels@gandrass.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

/**
 * Type that represents a single floor, available on the deployment map
 */
export type FloorMetadata = {
    title: string;
    value: number;
    icon: string;
}

/**
 * All available floors
 */
export class Floor {

    /**
     * The basement of the building, also called logistics level
     */
    public static Basement: FloorMetadata = {
        title: 'Basement',
        value: -1,
        icon: 'mdi-numeric-negative-1',
    }

    /**
     * The ground floor of the building, also called lobby level
     */
    public static GroundFloor: FloorMetadata = {
        title: 'Ground Floor',
        value: 0,
        icon: 'mdi-numeric-0',
    };

    /**
     * The intermediate floor between the ground floor and the first floor
     */
    public static IntermediateFloor: FloorMetadata = {
        title: 'Intermediate Floor',
        value: 100,
        icon: 'mdi-fraction-one-half',
    }

    /**
     * The first floor of the building
     */
    public static FirstFloor: FloorMetadata = {
        title: 'First Floor',
        value: 1,
        icon: 'mdi-numeric-1',
    }

    /**
     * The second floor of the building
     */
    public static SecondFloor: FloorMetadata = {
        title: 'Second Floor',
        value: 2,
        icon: 'mdi-numeric-2',
    }

    /**
     * The third floor of the building
     */
    public static ThirdFloor: FloorMetadata = {
        title: 'Third Floor',
        value: 3,
        icon: 'mdi-numeric-3',
    }

    /**
     * The fourth floor of the building
     */
    public static FourthFloor: FloorMetadata = {
        title: 'Fourth Floor',
        value: 4,
        icon: 'mdi-numeric-4',
    }

    /**
     * Returns the floor corresponding to the given value
     *
     * @param value The value of the floor
     * @
     */
    public static get(value: number): FloorMetadata|null {
        switch (value) {
            case -1: return Floor.Basement;
            case 0: return Floor.GroundFloor;
            case 100: return Floor.IntermediateFloor;
            case 1: return Floor.FirstFloor;
            case 2: return Floor.SecondFloor;
            case 3: return Floor.ThirdFloor;
            case 4: return Floor.FourthFloor;
            default: return null; // Invalid floor value
        }
    }

    /**
     * Retrieves all available floors in their desired display order
     */
    public static getAll(): FloorMetadata[] {
        return [
            Floor.Basement,
            Floor.GroundFloor,
            Floor.IntermediateFloor,
            Floor.FirstFloor,
            Floor.SecondFloor,
            Floor.ThirdFloor,
            Floor.FourthFloor,
        ];
    }

    /**
     * Returns the a list of all valid floor values
     *
     * @return {number[]} An array of all valid floor values
     */
    public static getAllValues(): number[] {
        return Floor.getAll().map(floor => floor.value);
    }

}
