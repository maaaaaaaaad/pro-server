import { Column, Entity, OneToMany } from 'typeorm'
import { CoreEntity } from '../../common/entities/core.entity'
import { IsEnum } from 'class-validator'
import { ItemEntity } from './item.entity'
import { ApiProperty } from '@nestjs/swagger'

export enum CategoryValues {
  BUY = 'BUY',
  SELL = 'SELL',
}

@Entity({ name: 'CATEGORY' })
export class CategoryEntity extends CoreEntity {
  @Column({ name: 'VALUE', enum: CategoryValues, nullable: false })
  @IsEnum(CategoryValues)
  @ApiProperty({
    description: 'Category values. please you select that buy or sell',
    enum: CategoryValues,
    nullable: false,
    required: true,
    examples: [CategoryValues.BUY, CategoryValues.SELL],
  })
  value: CategoryValues

  @OneToMany(() => ItemEntity, (item) => item.category)
  items: ItemEntity[]
}
