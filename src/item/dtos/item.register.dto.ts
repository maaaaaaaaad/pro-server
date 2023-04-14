import { ApiProperty, PickType } from '@nestjs/swagger'
import { ItemEntity } from '../entities/item.entity'
import { CategoryValues } from '../entities/category.entity'
import { CoreOutputDto } from '../../common/dtos/core.output.dto'

export class ItemRegisterInputDto extends PickType(ItemEntity, [
  'subject',
  'description',
  'coverImage',
  'price',
]) {
  @ApiProperty({
    description: 'Category values. please you select that buy or sell',
    enum: CategoryValues,
    nullable: false,
    required: true,
    examples: [CategoryValues.BUY, CategoryValues.SELL],
  })
  categoryValue: CategoryValues
}

export type ItemRegisterOutputDto = CoreOutputDto
