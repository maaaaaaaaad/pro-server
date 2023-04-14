import { Column, Entity, ManyToOne, OneToMany } from 'typeorm'
import { CoreEntity } from '../../common/entities/core.entity'
import { CategoryEntity } from './category.entity'
import { IsNotEmpty, IsNumber, IsString } from 'class-validator'
import { UserEntity } from '../../auth/entities/user.entity'
import { ApiProperty } from '@nestjs/swagger'
import { CommentEntity } from '../../comment/entities/comment.entity'

@Entity({ name: 'ITEM' })
export class ItemEntity extends CoreEntity {
  @ManyToOne(() => CategoryEntity, (category) => category.items, {
    onDelete: 'CASCADE',
    eager: true,
  })
  category: CategoryEntity

  @Column({ name: 'SUBJECT', nullable: false })
  @IsString()
  @IsNotEmpty()
  @ApiProperty({
    description: 'Item subject',
    type: String,
    example: 'WMD',
    nullable: false,
    required: true,
  })
  subject: string

  @Column({ name: 'COVER_IMAGE', nullable: false })
  @IsString()
  @IsNotEmpty()
  @ApiProperty({
    description: 'Item cover image',
    type: String,
    nullable: false,
    required: true,
    format: 'binary',
  })
  coverImage: string

  @Column({ name: 'DESCRIPTION', nullable: false })
  @IsString()
  @IsNotEmpty()
  @ApiProperty({
    description: 'Item description',
    type: String,
    nullable: false,
    example: 'This is description',
    required: true,
  })
  description: string

  @Column({ name: 'PRICE', nullable: false })
  @IsNumber()
  @IsNotEmpty()
  @ApiProperty({
    description: 'Item price',
    type: Number,
    nullable: false,
    example: 5000,
    required: true,
  })
  price: number

  @ManyToOne(() => UserEntity, (user) => user.items, {
    onDelete: 'CASCADE',
    eager: true,
  })
  owner: UserEntity

  @OneToMany(() => CommentEntity, (comment) => comment.item)
  comments: CommentEntity[]
}
