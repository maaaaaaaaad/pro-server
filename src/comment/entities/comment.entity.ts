import { Column, Entity, ManyToOne, RelationId } from 'typeorm'
import { CoreEntity } from '../../common/entities/core.entity'
import { IsNotEmpty, IsString, Length } from 'class-validator'
import { UserEntity } from '../../auth/entities/user.entity'
import { ItemEntity } from '../../item/entities/item.entity'
import { ApiProperty } from '@nestjs/swagger'

@Entity({ name: 'COMMENT' })
export class CommentEntity extends CoreEntity {
  @Column({ name: 'CONTENT' })
  @IsString()
  @IsNotEmpty()
  @Length(1, 30)
  @ApiProperty({
    description: 'Comment content',
    type: String,
    example: 'Hello Comment!',
    nullable: false,
    required: true,
  })
  content: string

  @ManyToOne(() => UserEntity, (owner) => owner.comments, {
    onDelete: 'CASCADE',
  })
  owner: UserEntity

  @RelationId((comment: CommentEntity) => comment.owner)
  @ApiProperty({
    description: 'Owner primary key',
    type: Number,
    nullable: false,
    required: true,
  })
  ownerId: number

  @ManyToOne(() => ItemEntity, (item) => item.comments, {
    onDelete: 'CASCADE',
  })
  item: ItemEntity

  @RelationId((comment: CommentEntity) => comment.item)
  @ApiProperty({
    description: 'Item primary key',
    type: Number,
    nullable: false,
    required: true,
  })
  itemId: number
}
